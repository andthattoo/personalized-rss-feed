import streamlit as st
from firstbatch import FirstBatch, AlgorithmLabel, Pinecone, Config, UserAction, Signal
import pinecone
from markdowns import css_, sidebar

FIRST_BATCH_API_KEY = st.secrets["api"]["firstbatch_api_key"]
PINECONE_API_KEY = st.secrets["api"]["pinecone_api_key"]
PINECONE_ENV = st.secrets["api"]["pinecone_env"]
CUSTOM_ALGO_ID = st.secrets["custom_algo_id"]


def display_feed_item():
    for i, b in enumerate(st.session_state.batches):
        image_url = b.data["img_link"]
        link_url = b.data["link"]
        title = b.data["title"]
        text = b.data["text"]

        with st.container():
            st.markdown(css_, unsafe_allow_html=True)

            st.markdown(f"""
                <div class="rss-item">
                    <img src="{image_url}" alt="Image Description">
                    <div class="rss-content">
                        <h2><a href="{link_url}">{title}</a></h2>
                        <p>{text + "..."}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Check if this id is already in the liked items
        if st.button(f'Like', i):
            signal(st.session_state.ids[i])
            st.session_state.likes.append(b)


def display_sidebar():
    st.sidebar.title("RSS Feed Algorithm")
    st.sidebar.markdown(sidebar)

    # Display signalled (liked) items
    st.sidebar.subheader("Liked Items")
    for item in st.session_state.likes:
        title = item.data["title"]
        link_url = item.data["link"]
        st.sidebar.markdown(f"[{title}]({link_url})")


# Add liked contents as signals, shaping embeddings
def signal(cid):
    st.session_state.personalized.add_signal(st.session_state.session, UserAction(Signal.LIKE), cid)


def main():
    st.title("Personalized RSS Feed")

    # Initialize Pinecone and FirstBatch

    if 'personalized' not in st.session_state:
        config = Config(batch_size=10, verbose=True, enable_history=True)
        personalized = FirstBatch(api_key=FIRST_BATCH_API_KEY, config=config)
        pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
        index = pinecone.Index("rss-2")
        personalized.add_vdb("rss_db", Pinecone(index, embedding_size=384))
        st.session_state.personalized = personalized

        st.session_state.session = st.session_state.personalized.session(AlgorithmLabel.CUSTOM, vdbid="rss_db",custom_id=CUSTOM_ALGO_ID)

        st.session_state.batches = []
        st.session_state.ids = []
        st.session_state.likes = []
        ids, batch = st.session_state.personalized.batch(st.session_state.session)
        st.session_state.batches += batch
        st.session_state.ids += ids

    display_feed_item()
    display_sidebar()

    # If "Load more" button is clicked, fetch new personalized batches
    if st.button("Load more"):
        ids, batch = st.session_state.personalized.batch(st.session_state.session)
        st.session_state.batches += batch
        st.session_state.ids += ids
        st.experimental_rerun()


if __name__ == '__main__':
    main()