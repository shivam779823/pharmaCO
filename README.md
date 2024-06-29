# PharmaCO - Pharmacy Management System

Pharmaco is a modern and intuitive Pharmacy Management System built using Flask. It provides a comprehensive solution for managing pharmacy operations such as inventory management, sales tracking, user authentication, and generating reports.


[![CI Pipeline - release](https://github.com/shivam779823/pharmaCO/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/shivam779823/pharmaCO/actions/workflows/release.yml)

[![CI Pipeline - PR ](https://github.com/shivam779823/pharmaCO/actions/workflows/release.yml/badge.svg?branch=dev)](https://github.com/shivam779823/pharmaCO/actions/workflows/PR.yml)


![CI/PR Build Version](https://img.shields.io/badge/CI/PR%20Build-v1.${{github.run_number}}-blue)

[![CodeQL](https://github.com/MichaelCurrin/badge-generator/workflows/CodeQL/badge.svg)](https://github.com/MichaelCurrin/badge-generator/actions?query=workflow%3ACodeQL "Code quality workflow status")

## UI
![image](https://github.com/shivam779823/pharmaCO/assets/105196334/2c56cce2-9d8c-44a8-83db-0ee82448ebb2)

### Login Page
![image](https://github.com/shivam779823/pharmaCO/assets/105196334/780ecd50-2ba9-4a5f-921f-c09e696f70f7)

### Analytics by Metabase
![Screenshot 2024-06-24 172846](https://github.com/shivam779823/pharmaCO/assets/105196334/031d52a2-7438-4f90-876b-0244c2ea8baa)

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Routes](#routes)
- [Metrics](#metrics)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Medince database**: handles small pharmacies stores medicines records and expires , out of stocks medicines effectively.
- **Inventory Management**: Add, remove, update, and search medicines in the inventory.
- **Sales Management**: Sell medicines to customers, generate invoices, and track transactions.
- **Report Generation**: Generate PDF reports for inventory and transactions within a specified date range.
- **Metrics Monitoring**: Monitor HTTP request metrics and response latencies using Prometheus.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/shivam779823/pharmaCO.git
```

2. Setup MySQL server and configure mysql connection in app.py

3. Install dependencies:

```
pip install -r requirements.txt
```
4. Run 

```
python app.py
```

## Contributing 

Contributions to the Pharmacy Management System are welcome! If you find any issues or have ideas for improvements, feel free to open an issue or submit a pull request.


## Acknowledgments 

Special thanks to OpenAI for providing the AI technology used in this project.

Thanks to the Flask community for the web framework.

Icon credits: Font Awesome.

Contact For any inquiries or support, please connenct with me @shivam.

## PharmaCo - Empowering pharmacies with modern management solutions.




