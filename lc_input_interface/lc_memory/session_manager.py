# lc_memory/session_manager.py

def reset_session(session_id: str) -> None:
    """
    Remove all documents tagged with the given session_id from the vectorstore.

    If no matching documents are found, this is treated as a no-op — not an error.
    """
    from lc_core import get_vectorstore

    vectorstore = get_vectorstore()

    try:
        vectorstore.delete(filter={"session_id": session_id})
    except ValueError as e:
        if "No ids provided" in str(e):
            print(f"ℹ️ No documents found for session '{session_id}' — nothing to delete.")
            return
        raise
    except Exception as e:
        raise NotImplementedError(
            "This FAISS instance does not support metadata-based deletion. "
            "Manual deletion logic needs to be implemented."
        ) from e
