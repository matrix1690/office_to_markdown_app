import os
import tempfile
import re

import streamlit as st
from markitdown import MarkItDown

# Set page configuration
st.set_page_config(
    page_title="Office to Markdown",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Newer, more capable converters to promote alongside this demo app
WEB_CONVERTER_URL = "https://pythonandvba.com/office-to-markdown-converter/"
DESKTOP_APP_URL = "https://pythonandvba.com/office2md"


# Helper functions
def get_file_extension(filename):
    """Extract the file extension from a filename."""
    return filename.rsplit(".", 1)[1].lower() if "." in filename else ""


def is_youtube_url(url):
    """Check if a URL is a valid YouTube URL."""
    youtube_regex = r"^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$"
    return bool(re.match(youtube_regex, url))


def extract_youtube_id(url):
    """Extract the YouTube video ID from a URL."""
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",  # Standard YouTube URLs
        r"(?:youtu\.be\/)([0-9A-Za-z_-]{11})",  # Short YouTube URLs
        r"(?:embed\/)([0-9A-Za-z_-]{11})",  # Embedded YouTube URLs
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def convert_file_to_markdown(file_data, filename):
    """
    Convert a file to Markdown using MarkItDown.

    Args:
        file_data: The binary content of the file
        filename: The name of the file

    Returns:
        Tuple of (markdown_content, error_message)
    """
    try:
        # Create a temporary file
        ext = get_file_extension(filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp_file:
            tmp_file.write(file_data)
            tmp_file_path = tmp_file.name

        # Initialize MarkItDown and convert the file
        md = MarkItDown(enable_plugins=False)
        result = md.convert(tmp_file_path)

        # Clean up the temporary file
        os.unlink(tmp_file_path)

        return result.text_content, None
    except Exception as e:
        return "", str(e)


def convert_youtube_to_markdown(url):
    """
    Convert a YouTube URL to Markdown using MarkItDown.

    Args:
        url: The YouTube URL

    Returns:
        Tuple of (markdown_content, error_message)
    """
    try:
        # Initialize MarkItDown and convert the URL
        md = MarkItDown(enable_plugins=False)
        result = md.convert(url)

        return result.text_content, None
    except Exception as e:
        return "", str(e)


def get_supported_formats():
    """
    Get a dictionary of supported file formats categorized by type.

    Returns:
        Dictionary of supported formats
    """
    return {
        "📝 Documents": {
            "formats": ["Word (.docx, .doc)", "PDF", "EPub"],
            "extensions": ["docx", "doc", "pdf", "epub"],
        },
        "📊 Spreadsheets": {
            "formats": ["Excel (.xlsx, .xls)"],
            "extensions": ["xlsx", "xls"],
        },
        "📊 Presentations": {
            "formats": ["PowerPoint (.pptx, .ppt)"],
            "extensions": ["pptx", "ppt"],
        },
        "🌐 Web": {"formats": ["HTML", "YouTube URLs"], "extensions": ["html", "htm"]},
        "📁 Others": {
            "formats": ["CSV", "JSON", "XML", "ZIP (iterates over contents)"],
            "extensions": ["csv", "json", "xml", "zip"],
        },
    }


def render_promo_banner():
    """Render a banner promoting the newer web and desktop converters."""
    with st.container(border=True):
        st.markdown("#### 🚀 Newer & better versions available!")
        st.markdown(
            "This app is a simple demo. For more formats, more features, "
            "and a smoother experience, check out my newer tools:"
        )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "**🌐 Free Online Converter**  \n"
                "20+ formats (Word, Excel, PowerPoint, PDF, Outlook & more) — "
                "drag & drop, no install or sign-up needed."
            )
            st.link_button(
                "Try the Online Converter",
                WEB_CONVERTER_URL,
                use_container_width=True,
                type="primary",
            )
        with col2:
            st.markdown(
                "**🖥️ Office2MD Desktop App**  \n"
                "Runs 100% locally — your files never leave your computer. "
                "Batch conversion & offline OCR included."
            )
            st.link_button(
                "Get the Desktop App",
                DESKTOP_APP_URL,
                use_container_width=True,
            )


def main():
    # Initialize session state
    if "markdown_content" not in st.session_state:
        st.session_state.markdown_content = ""
    if "file_name" not in st.session_state:
        st.session_state.file_name = ""

    # Header
    st.title("Office to Markdown")
    st.image("OfficeToMD_Logo.png")

    render_promo_banner()

    # Sidebar
    with st.sidebar:
        st.title("Office to MD")
        st.image("OfficeToMD_Logo.png", width=150)

        # Supported formats in an expander
        with st.expander("Supported Formats"):
            formats = get_supported_formats()
            for category, info in formats.items():
                st.write(f"**{category}**")
                for format_name in info["formats"]:
                    st.write(f"- {format_name}")

        # Promote the newer converters
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🚀 Better Converters")
        st.sidebar.markdown(
            f"🌐 [Free Online Converter]({WEB_CONVERTER_URL})  \n"
            "More formats, no install or sign-up"
        )
        st.sidebar.markdown(
            f"🖥️ [Office2MD Desktop App]({DESKTOP_APP_URL})  \n"
            "100% offline & private, batch conversion"
        )

        # Add branding at the bottom of the sidebar
        st.sidebar.markdown("---")

        st.sidebar.markdown(
            "Created with ❤️ by [Sven Bosau](https://www.linkedin.com/in/sven-bosau/)"
        )

        st.sidebar.markdown("### Connect with me")
        st.sidebar.markdown("🌍 [Website](https://pythonandvba.com)")
        st.sidebar.markdown("📺 [YouTube](https://youtube.com/@codingisfun)")
        st.sidebar.markdown("💼 [LinkedIn](https://www.linkedin.com/in/sven-bosau/)")

    # File upload
    all_extensions = []
    formats = get_supported_formats()
    for category, info in formats.items():
        all_extensions.extend(info["extensions"])

    uploaded_file = st.file_uploader(
        "Upload a file to convert",
        type=all_extensions,
        help="Select a file to convert to Markdown",
    )

    # YouTube URL input
    youtube_url = st.text_input(
        "Or enter a YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Enter a YouTube URL to convert its transcript to Markdown",
    )

    # Convert button
    if st.button("Convert to Markdown", use_container_width=True, type="primary"):
        if not uploaded_file and not youtube_url:
            st.error("Please upload a file or enter a YouTube URL")
        elif youtube_url and not is_youtube_url(youtube_url):
            st.error("Please enter a valid YouTube URL")
        else:
            with st.spinner("Converting to Markdown..."):
                if uploaded_file:
                    # Convert uploaded file
                    markdown_content, error = convert_file_to_markdown(
                        uploaded_file.getbuffer(), uploaded_file.name
                    )

                    if error:
                        st.error(f"Error during conversion: {error}")
                    else:
                        st.session_state.markdown_content = markdown_content
                        st.session_state.file_name = uploaded_file.name
                        st.success("Conversion completed successfully!")

                elif youtube_url:
                    # Convert YouTube URL
                    markdown_content, error = convert_youtube_to_markdown(youtube_url)

                    if error:
                        st.error(f"Error during conversion: {error}")
                    else:
                        # Extract video ID from URL for naming
                        video_id = extract_youtube_id(youtube_url)
                        file_name = (
                            f"youtube_{video_id}.md" if video_id else "youtube_video.md"
                        )

                        st.session_state.markdown_content = markdown_content
                        st.session_state.file_name = file_name
                        st.success("Conversion completed successfully!")

    # Results section
    if st.session_state.markdown_content:
        st.divider()

        # Download button
        file_name = st.session_state.file_name.rsplit(".", 1)[0] + ".md"

        st.download_button(
            label="Download Markdown File",
            data=st.session_state.markdown_content,
            file_name=file_name,
            mime="text/markdown",
            use_container_width=True,
        )

        # Preview
        st.subheader("Preview")
        preview_content = st.session_state.markdown_content[:2000]
        if len(st.session_state.markdown_content) > 2000:
            preview_content += (
                "...\n\n(Preview truncated. Download the full file to see all content.)"
            )

        st.text_area(label="", value=preview_content, height=400, disabled=True)


if __name__ == "__main__":
    main()
