import streamlit as st
from firstbatch import FirstBatch, AlgorithmLabel, Pinecone, Config, UserAction, Signal
import pinecone

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
            st.markdown("""
                <style>
                    .rss-item {
                        display: flex;
                        flex-direction: row;
                        border: 1px solid #e0e0e0;
                        border-radius: 5px;
                        margin: 10px 0;
                        padding: 15px;
                        transition: box-shadow 0.3s ease;
                    }
                    .rss-item:hover {
                        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                    }
                    .rss-item img {
                        width: 300px;
                        height: 300px;
                        border-radius: 5px;
                        object-fit: cover;
                        margin-right: 15px;
                    }
                    .rss-content {
                        flex-grow: 1;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                    }
                    .rss-content h2 {
                        font-size: 1.5em;
                        margin: 0;
                        color: #333;
                    }
                    .rss-content p {
                        color: #777;
                        line-height: 1.5;
                        margin-top: 5px;
                    }
                </style>
            """, unsafe_allow_html=True)

            # Using the CSS with Streamlit's markdown
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
    lurl = "https://firstbatch.gitbook.io/firstbatch-sdk/get-started/introduction"
    st.sidebar.markdown(f"""
    The recommendation algorithm uses embeddings for personalization. Here's a breakdown:
    Level 1: Initial state of the algorithm. Content is fully randomized.

    Level 2: Tightly anchored to signals, introducing minimal variations and randomness. It pulls content closely aligned with current signals.

    Level 3: Leverages signals while integrating elements of randomness and exploration. It retrieves content that resonates with current signals and content that is contextually linked to these signals. 

    Level 4: Strongly add elements of randomness and exploration. It retrieves content that resembles with current signals but nudged into new directions.

    For all nodes,  Only the last three signals influence the calculation of embeddings, ensuring that personalization is influenced predominantly by recent interactions.

    Algorithm in [detail](https://firstbatch.gitbook.io/rss-feed-algorithm/)

    For SDK Reference: [FirstBatch SDK Docs]({lurl})

    """)

    # Display signalled (liked) items
    st.sidebar.subheader("Liked Items")
    for item in st.session_state.likes:
        title = item.data["title"]
        link_url = item.data["link"]
        st.sidebar.markdown(f"[{title}]({link_url})")


def signal(cid):
    st.session_state.personalized.add_signal(st.session_state.session, UserAction(Signal.LIKE), cid)


def main():
    st.title("Personalized RSS Feed")

    # Initialize Pinecone and other services

    if 'personalized' not in st.session_state:
        config = Config(batch_size=10, verbose=True, enable_history=True, embedding_size=384)
        personalized = FirstBatch(api_key=FIRST_BATCH_API_KEY, config=config)
        pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
        index = pinecone.Index("rss-2")
        personalized.add_vdb("rss_db", Pinecone(index))
        st.session_state.personalized = personalized

        st.session_state.session = st.session_state.personalized.session(AlgorithmLabel.CUSTOM,
                                                                         vdbid="rss_db",
                                                                         custom_id=CUSTOM_ALGO_ID)

        st.session_state.batches = []
        st.session_state.ids = []
        st.session_state.likes = []
        ids, batch = st.session_state.personalized.batch(st.session_state.session)
        st.session_state.batches += batch
        st.session_state.ids += ids

    display_feed_item()
    display_sidebar()

    # If "Load more" button is clicked, increase the batch count and rerun the app to fetch more data
    if st.button("Load more"):
        ids, batch = st.session_state.personalized.batch(st.session_state.session)
        st.session_state.batches += batch
        st.session_state.ids += ids
        st.experimental_rerun()


if __name__ == '__main__':
    main()