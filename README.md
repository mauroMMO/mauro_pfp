## Survey Instruments

All the survey instruments are present in the folder "survey instruments". Both versions of the survey are present, alternating human and ai generated Evidence Briefings.

## How to Run the Project

Follow the steps below to run the application:

1. The virtual environment for this project is managed using **Conda**. Make sure Conda is installed on your system beforehand:  
   [https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html]


2. The `environment.yml` file contains a list of all packages required to run the project.  
   Create the Conda environment using the command below:

   ```bash
   conda env create -f environment.yml
3. Create a file named `env.env` in the root of the project, following the structure provided in the included `env-sample.env`.

   > **Note:** You must correctly insert your OpenAI API key into this new file.  
   > If you don’t have an API key yet, follow the steps below:

   3.1. **Create an OpenAI Account**  
        The first step is to create an account on the OpenAI platform. Follow the steps below:
        
        - Go to the [OpenAI website](https://platform.openai.com/).
        - Click **"Sign Up"** in the top-right corner of the page.
        - Fill in the required fields with your information, or log in using your Google account.

   3.2. **Access the API Keys Section**  
        After creating your account and logging in, go to the section where API keys are generated:

        - In the main OpenAI dashboard, click **"API"** in the left-hand menu.
        - Then click **"API Keys"**.

   3.3. **Create a New API Key**  
        Now, let's create your API key:

        - Click the button **"Create new secret key"**.
        - Give it a name that helps you identify it later (e.g., "briefing tool").
        - Click **"Create secret key"**.

   3.4. **Copy and Save Your API Key**  
        After creating the key, OpenAI will display it **only once**.  
        Make sure to copy and save it in a safe place. If you lose it, you will need to generate a new one.


4. Now you need to activate the Conda environment. Run the following command:

   ```bash
   conda activate gerador_evidence_briefings

5. To run the application, use the following command:

   ```bash
   streamlit run main.py