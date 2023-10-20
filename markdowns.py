css_ = """
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

    /* Mobile */
    @media only screen and (max-width: 600px) {
        .rss-item {
            flex-direction: column;
            align-items: center;
        }
        .rss-item img {
            width: 100%;
            height: auto;
            margin-right: 0;
            margin-bottom: 15px;
        }
    }
</style>
"""


sidebar = """
    The recommendation algorithm uses embeddings for personalization. Here's a breakdown:
    Level 1: Initial state of the algorithm. Content is fully randomized.

    Level 2: Tightly anchored to signals, introducing minimal variations and randomness. It pulls content closely aligned with current signals.

    Level 3: Leverages signals while integrating elements of randomness and exploration. It retrieves content that resonates with current signals and content that is contextually linked to these signals. 

    Level 4: Strongly add elements of randomness and exploration. It retrieves content that resembles with current signals but nudged into new directions.

    For all nodes,  Only the last three signals influence the calculation of embeddings, ensuring that personalization is influenced predominantly by recent interactions.

    Algorithm in [detail](https://firstbatch.gitbook.io/rss-feed-algorithm/)

    For SDK Reference: [FirstBatch SDK Docs](https://firstbatch.gitbook.io/firstbatch-sdk/get-started/introduction)

    """