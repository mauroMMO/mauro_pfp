from data_loader import DataLoader
import os
import pandas as pd
import evaluate


class Evaluator:
    
    def __init__(self):
        self.rouge = evaluate.load('rouge')
        self.bleu = evaluate.load('bleu')
        self.meteor = evaluate.load('meteor')
        pass

    def create_eval_dataset(self, data_loader):
        """
        Create a new evaluation dataset , considering the articles present in the "x" folder
        and the human-made Evidence Briefings present in the "y" folder. Both directories are present inside 
        the "briefings" folder. The json is formatted as follows:
        {"id":"01","article":"<article text>","reference":"<human made evidence briefing text>"} 
        """


        articles_dir = os.path.join('briefings', 'x')
        briefs_dir = os.path.join('briefings', 'y')
        output_csv_name = "eval_dataset.csv"
        output_path = os.path.join(os.getcwd(), output_csv_name)
        if os.path.exists(output_path):
            return

        data_for_df = []

    
        article_files = sorted(
            [f for f in os.listdir(articles_dir) if f.lower().endswith('.pdf')],
            key=lambda name: int(os.path.splitext(name)[0])
        )

        for filename in article_files:
            article_filepath = os.path.join(articles_dir, filename)
            brief_filepath = os.path.join(briefs_dir, filename)

            if os.path.isfile(brief_filepath):
                print(f"Processando par: {filename}")
                
                
                article_text = data_loader.load_single_pdf(article_filepath)
                brief_text = data_loader.load_single_pdf(brief_filepath)

                if article_text and brief_text:
                    data_for_df.append({'article': article_text, 'brief': brief_text})
                else:
                    print(f"Aviso: Não foi possível extrair texto de um dos arquivos do par '{filename}'. Par ignorado.")
            else:
                print(f"Aviso: O briefing '{filename}' não foi encontrado em '{briefs_dir}'. Par ignorado.")

        if not data_for_df:
            print("Nenhum par de artigo/briefing válido foi encontrado. O CSV não foi gerado.")
            return

        df = pd.DataFrame(data_for_df)
        output_path = os.path.join(os.getcwd(), output_csv_name)
        df.to_csv(output_path, index=False, encoding='utf-8')
        
       
        print(f"Total de pares (linhas) no CSV: {len(df)}")


    def load_eval_dataset(self):
        """
        Load the evaluation dataset from the CSV file.
        """
        df = pd.read_csv("eval_dataset.csv", dtype=str)
        return df
    
    def evaluate(self,results_dataframe):
        """
        Calcula as métricas ROUGE, BLEU e METEOR a partir de um DataFrame.

        Args:
            results_dataframe (pd.DataFrame): DataFrame que deve conter as colunas
                                              'reference_brief' (gabarito) e
                                              'generated_brief' (predição do modelo).

        Returns:
            tuple: Um DataFrame com a coluna de score individual (rougeL_score)
                   e um dicionário com as pontuações agregadas.
        """

        # Extrai as listas para cálculo
        predictions = results_dataframe['generated_brief'].tolist()
        references = results_dataframe['brief'].tolist()
        # Calcula as pontuações agregadas
        rouge_scores = self.rouge.compute(predictions=predictions, references=references)
        bleu_scores = self.bleu.compute(predictions=predictions, references=references)
        meteor_scores = self.meteor.compute(predictions=predictions, references=references)
        
        aggregated_scores = {
            "ROUGE": rouge_scores,
            "BLEU": bleu_scores,
            "METEOR": meteor_scores
        }
        
        # Calcula ROUGE-L para cada linha individualmente e adiciona ao DF
        rouge_l_scores = []
        for pred, ref in zip(predictions, references):
            score = self.rouge.compute(predictions=[pred], references=[ref])
            rouge_l_scores.append(score['rougeL'])
            
        results_dataframe['rougeL_score'] = rouge_l_scores

        return results_dataframe, aggregated_scores


