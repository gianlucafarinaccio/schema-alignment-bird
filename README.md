# schema-alignment-bird

**Project:** "Big Data Integration" assignment - Advanced Topics in Computer Science 24/25 <br>
**Author:** Gianluca Farinaccio <br>

This repo presents a system that for each natural language question in the BIRD benchmark, identifies
the Source Tables (STs) that contain data relevant to answering the question.<br>
It's also evaluate the results against the BIRD ground truth computing the overall recall, precision,
and F1-score for detected STs.

This system rely primarily on LLMs (**Llama-3.3-70b-8192** in this case) to automate these steps.
I use the free tier of Groq to obtain an API access to LLM.

The selected dataset is **BIRD mini-dev** (500 queries from 10 different DBs).
The scripts are designed to be executed using Groq API free tier so the total execution time could be around 20 minutes for mini-dev.

## Project Structure

 >\src: source files to execute queries and evaluate metrics<br>
 >\dataset: mini-dev BIRD dataset	and DBs schema<br>
 >\output_<your_bench_name>: all results and metrics of your execution<br>

## Results
This system obtain the following metrics using **Llama-3.3-70b-8192** and **mini-dev** as dataset. More information and detailed metrics for each DB can be found in *"output_bench_25032025"* directory.

> * recall: 0.7758186397984886
> * precision: 0.6829268292682927
> * F1-score: 0.7264150943396226

## Installation

* clone repo
```bash 
git clone https://github.com/gianlucafarinaccio/schema-alignment-bird.git 
```

* create your virtualenv
```bash 
python3 -m venv <env-name>
```
* activate virtualenv
```bash 
source <env-name>/bin/activate
```

* install dependencies via pip
```bash 
pip install -r requirements.txt
```

* setup Groq API key via ENV variable 
```bash 
export GROQ_API_KEY=<your-api-key-here>
```

## Execute

* execute main script 
```bash 
python3 src/main.py --name <bench_name>
```

* calculate metrics 
```bash 
python3 src/metrics.py --name <bench_name>
```