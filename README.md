
<!-- PROJECT OVERVIEW -->
<br />
  <h1 align="center">PickPocket</h1>
  <p align="center">
    A python script to transfer all your Pocket links to a database in Notion. 
    <br />
    <a href="https://github.com/paperboi/PickPocket">Explore the docs</a>
    ·
    <a href="https://github.com/paperboi/PickPocket/issues">File issues and feature requests here</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

A python script to copy all your Pocket saves to a database in Notion. Current iteration is based off the HTML export option provided by the folks at Pocket.

**Intended for**
- Those who are looking to transfer their reading lists from Pocket to Notion.
- Those who want to keep track and analyze what they read.


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* A Pocket account to retreive your saved content from.
* A Notion account to store your links.
* Python 3 on your system to run the code.
  
### Setup & Installation
 
1. Clone this repository.
    ```sh
    git clone https://github.com/paperboi/PickPocket.git
    ```
2. Navigate to the directory and install the pre-requisite packages using
   ```sh
   pip install -r requirements.txt
   ```

<!-- USAGE EXAMPLES -->
## Usage
1. Export your Pocket saves from [here](https://help.getpocket.com/article/1015-exporting-your-pocket-list). Assign the path to this file to the variable `PATH_POCKET_FILE` in [pocket2notion.py](https://github.com/paperboi/PickPocket/blob/master/pocket2notion.py).
1. Duplicate this [database template](https://www.notion.so/personaljeff/e4a0751a114842c6b2b238218e52e7d2?v=062127a6aa4341fb98e6d74b0eadfc4c) to your Notion workspace. Copy-paste the database address to the `NOTION_TABLE_ID` variable in [pocket2notion.py](https://github.com/paperboi/PickPocket/blob/master/pocket2notion.py)
2. Since this code requires access of non-public pages, an authentication token from your Notion page is required. This token is stored in the `token_v2` cookie. This can be found in the `storage` tab of your browser's developer tools.
   - For Chrome: Open Developer Tools (*Menu > Other tools > Developer Tools*), navigate to Application tab and go to *Storage\Cookies* to find the token.
   - Assign this `token_v2` value to the `NOTION_TOKEN` variable in [pocket2notion.py](https://github.com/paperboi/PickPocket/blob/master/pocket2notion.py).

To use the script, navigate to the directory and run
   ```
   python pocket2notion.py 
  ```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/paperboi/PickPocket/issues) for a list of proposed features (and known issues).


<!-- CONTRIBUTING -->
## Contributing

<!-- Contributions are what make the open source community such an amazing place to be learn, inspire, and create. -->
Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Jeffrey Jacob - [@DullBlackWall](https://twitter.com/DullBlackWall) - jeffreysamjacob@gmail.com

Project Link: [https://github.com/paperboi/PickPocket](https://github.com/paperboi/PickPocket)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [K.P. Govind](https://github.com/reisub0) for clearing my doubts every step of the way.
* [Jamie Alexandre](https://github.com/jamalex/) for the powerful [notion-py](https://github.com/jamalex/notion-py) API.
