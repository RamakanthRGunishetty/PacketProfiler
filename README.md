# PacketProfiler

PacketProfiler is a web-based tool for network traffic analysis and classification using machine learning techniques. This application allows users to upload PCAP (network capture) files and provides detailed insights into network flows.

## Features

- PCAP file upload and analysis
- Automatic feature extraction from network traffic
- Traffic classification using machine learning models:
  - Decision Tree
  - K-Nearest Neighbors (KNN)
  - Random Forest
- Visualization of results with classification reports and confusion matrices
- User-friendly web interface

## Tech Stack

- Backend: Python, Flask
- Frontend: HTML, CSS
- Machine Learning: Scikit-learn (pre-trained models)
- Network Analysis: pyshark

## Installation

1. Clone the repository
2. Set up a virtual environment (optional but recommended)
3. Install the required dependencies
   ## Usage

1. Start the Flask application:

2. Open a web browser and navigate to `http://localhost:5000`

3. Upload a PCAP file using the web interface

4. View the analysis results, including flow classifications and visualizations

## Project Structure

- `app.py`: Main Flask application file
- `feature_extraction.py`: Contains functions for extracting features from PCAP files
- `templates/`: HTML templates for the web interface
- `static/`: Static files (CSS, images)
- `uploads/`: Temporary directory for uploaded PCAP files

## Contributing

Contributions to PacketProfiler are welcome! Please feel free to submit a Pull Request.

## Contact

Sathwik Madhusudan - [sathwikmadhusudan@gmail.com](mailto:sathwikmadhusudan@gmail.com)

Project Link: [https://github.com/Sathwik-Madhusudan/PacketProfiler](https://github.com/Sathwik-Madhusudan/PacketProfiler)
