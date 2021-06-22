<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project
    
The aim of the project is to prepare the current dashboard for the future. To guarantee this, it was decided to run the entire dashboard on Python instead of R, which is the current language of the dashboard. With this major change also a requirement of the dashboard would become an almost exact copy to the Front-End and thus the users will not see any difference.

### Technology Stack

 Technologies | 
--- |
Flask: Python |
Dash: Python |
Dash Plotly  |
Microsoft SQL Server |
Pandas Dataframe |

<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Sagi10/Project-Bigdata.git
   ```
2. Create a Environment
   ```sh
    Globaly install virtualenv via pip: pip install virtualenv
    Go to project folder and create virtualenv: virtualenv <environmentName>
   ```
3. Activate environment
   ```sh
   <environmentName>\Scripts\activate (Windows)
   source <environmentName>/bin/activate (Mac)
   ```
4. Install all Python dependecies like Flask, Dash via PIP
   ```JS
    pip install -r requirments.txt  
   ```
5. Set your own Database connection string in your system variable DATABASE_URL or in the config.py file
6. Run the (Flask)Application: 
    ```JS
    flask run 
   ```
   (The main class it already defined in the '.flaskenv' file)
   The flask server should start together with the database on localhost:5000   

    ![alt text](https://i.imgur.com/928bl4k.png "Logo Title Text 1")

7. When you have PIP'ed something new the requirments.txt need to be updated as well - Pick all Pip modules that has been installed and place it into a file called requirmnet.txt  
(First activate environment)
   ```JS
    pip freeze > requirements.txt
   ```

<!-- LICENSE -->
## License
Distributed under the MIT License.


