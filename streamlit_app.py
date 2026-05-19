import os

import isodate
import pandas as pd
import streamlit as st
from googleapiclient.discovery import build


def extract_video_id(value):
    value = value.strip()
    if not value:
        return None

    # 이미 비디오 ID만 입력한 경우
    if len(value) >= 11 and 'youtube' not in value and 'youtu.be' not in value:
        return value

    try:
        from urllib.parse import parse_qs, urlparse

        parsed = urlparse(value)
        if parsed.hostname in ('youtu.be', 'www.youtu.be'):
            return parsed.path.lstrip('/')
        if parsed.hostname in ('youtube.com', 'www.youtube.com', 'm.youtube.com'):
            if parsed.path == '/watch':
                query = parse_qs(parsed.query)
                return query.get('v', [None])[0]
            if parsed.path.startswith('/embed/'):
                return parsed.path.split('/')[2]
            if parsed.path.startswith('/shorts/'):
                return parsed.path.split('/')[2]
    except Exception:
        return None

    return None


def fetch_video_data(api_key, video_ids):
    youtube = build("youtube", "v3", developerKey=api_key)
    all_videos = []

    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i : i + 50]
        response = (
            youtube.videos()
            .list(part="snippet,statistics,contentDetails", id=','.join(batch_ids))
            .execute()
        )

        for video in response.get('items', []):
            video_id = video.get('id')
            snippet = video.get('snippet', {})
            stats = video.get('statistics', {})
            content = video.get('contentDetails', {})
            duration = content.get('duration', 'PT0S')

            duration_seconds = int(isodate.parse_duration(duration).total_seconds())
            minutes = duration_seconds // 60
            seconds = duration_seconds % 60

            all_videos.append({
                '채널명': snippet.get('channelTitle', ''),
                '링크': f"https://www.youtube.com/watch?v={video_id}",
                '제목(원본 제목)': snippet.get('title', ''),
                '제목(한국어 번역)': snippet.get('title', ''),
                '조회수': int(stats.get('viewCount', 0)),
                '좋아요': int(stats.get('likeCount', 0)),
                '댓글': int(stats.get('commentCount', 0)),
                '게시일': snippet.get('publishedAt', '')[:10],
                '영상 평균 길이': f"{minutes}:{seconds:02d}",
            })

    return pd.DataFrame(all_videos)


def fetch_channel_stats(api_key, channel_id):
    youtube = build("youtube", "v3", developerKey=api_key)
    response = (
        youtube.channels()
        .list(part='statistics', id=channel_id)
        .execute()
    )
    if response.get('items'):
        return response['items'][0].get('statistics', {})
    return {}


def main():
    st.title('🎯 YouTube Video Stats Collector')
    st.write('Paste YouTube URLs or video IDs below, one per line, then click **Fetch data**.')

    api_key = st.text_input(
        'YouTube API Key',
        value=os.getenv('YOUTUBE_API_KEY', ''),
        type='password',
        help='You can also set YOUTUBE_API_KEY in your environment.',
    )

    translate_checkbox = st.checkbox('자동 한국어 번역 (일본어 → 한국어)', value=False)

    video_ids_input = st.text_area(
        'Video IDs',
        height=220,
        placeholder='Enter one YouTube video ID per line',
    )

    if st.button('Fetch data'):
        video_ids = [line.strip() for line in video_ids_input.splitlines() if line.strip()]
        parsed_ids = []
        for value in video_ids:
            video_id = extract_video_id(value)
            if video_id:
                parsed_ids.append(video_id)

        if not api_key:
            st.error('API 키를 입력하거나 YOUTUBE_API_KEY 환경 변수를 설정하세요.')
            return

        if not parsed_ids:
            st.error('최소 하나의 YouTube 비디오 ID를 입력하세요.')
            return

        with st.spinner('데이터를 가져오는 중입니다...'):
            try:
                df = fetch_video_data(api_key, parsed_ids)

                if df.empty:
                    st.warning('요청한 비디오에서 데이터를 찾을 수 없습니다.')
                    return

                # 자동 번역이 켜져 있으면 제목을 일본어->한국어로 번역
                if translate_checkbox:
                    try:
                        from googletrans import Translator
                        translator = Translator()

                        def _safe_translate(text):
                            try:
                                if not text:
                                    return text
                                return translator.translate(text, dest='ko').text
                            except Exception:
                                return text

                        df['제목(한국어 번역)'] = df['제목(원본 제목)'].apply(_safe_translate)
                    except Exception:
                        st.warning('자동 번역을 사용하려면 `googletrans`를 설치하고 앱을 재시작하세요.')

                st.success(f'수집된 영상: {len(df)}개')
                st.write('### 데이터 미리보기')
                st.dataframe(df)

                st.write('### 엑셀 복사용 출력')
                tsv_text = df.to_csv(sep='\t', index=False)
                st.text_area('복사해서 엑셀에 붙여넣기', tsv_text, height=260)

                st.write('### 데이터 통계')
                stats_col1, stats_col2 = st.columns(2)
                stats_col1.metric('평균 조회수', f"{df['조회수'].mean():,.0f}")
                stats_col1.metric('최고 조회수', f"{df['조회수'].max():,}")
                stats_col2.metric('평균 좋아요', f"{df['좋아요'].mean():,.0f}")
                stats_col2.metric('총 댓글', f"{df['댓글'].sum():,}")

                first_channel_id = None
                if not df.empty:
                    first_channel_id = (
                        build('youtube', 'v3', developerKey=api_key)
                        .videos()
                        .list(part='snippet', id=parsed_ids[0])
                        .execute()
                        .get('items', [])[0]
                        .get('snippet', {})
                        .get('channelId')
                    )

                if first_channel_id:
                    channel_stats = fetch_channel_stats(api_key, first_channel_id)
                    if channel_stats:
                        st.write('### 채널 정보')
                        st.write(
                            {
                                '구독자': f"{int(channel_stats.get('subscriberCount', 0)):,}",
                                '영상 개수': f"{int(channel_stats.get('videoCount', 0)):,}",
                                '총 조회수': f"{int(channel_stats.get('viewCount', 0)):,}",
                            }
                        )

            except Exception as exc:
                st.error(f'데이터 수집 중 오류가 발생했습니다: {exc}')


if __name__ == '__main__':
    main()
