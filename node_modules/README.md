# AdvisorBert
A web service with a custom neural search engine that helps students to find research they will love doing.

## Problem
Choosing a laboratory for PhD and postdoctoral study is a common challenge amongst researching students. Often, the final decision is heavily influenced by the faculty of their alma mater, or else students choose to apply to the most prestigious university and select research topics based on who is available, not their own interest. This places students who are changing their specific topic of scientific work and students from unprivileged backgrounds who don’t have an opportunity for academic networking in their university in a disadvantaged position. This phenomenon of students choosing PhD programs without thorough prior research is one of the factors that explain the high PhD dropout rate. 

## Solution
To help students in making this decision, we have developed a special-purpose academic search engine. The application allows a student to input any specific topic they are interested in and get a map with all of the active researchers in the world who produced some work on the topic. Researchers are ranked by their impact index and links to their social media are provided. This allows students to broaden their scope of researchers working in their field of interest and find potential collaborators or advisors. 

Many of the best researchers do not reside in the highest ranking universities, and this tool allows students to find institutions that may not be on their radar. Importantly, this tool can help students who can’t get into top-ranking universities due to their background to still find a place to do good scientific work; it encourages students to conduct more research when continuing their education at the postgraduate level and makes their research process much easier. 

## How does it work

### Search algorithm
First we took a dataset of research articles with more than 20 citations published in the last three years - this amounted to around 700 thousand articles. We also downloaded their authors and their affiliations. We took all this data from [OpenAlex](https://openalex.org) - open source academic database. 

For each paper we took its abstract and used pretrained SBERT model downloaded from HuggingFace to calculate a document vector. We save the resulting file to disk and load it to memory when the application is launched. 

When we receive a search topic request we run the following algorithm:
Calculate a vector of a search query
Calculate cos similarity score between search query and all documents
Filter articles with cos similarity score bigger then some fixed threshold (which has been chosen empirically)
Then we calculate the number of relevant articles which have been written by each author - we define it as an author’s relevancy index. 
On a map we display authors with a relevancy index higher than a certain threshold. 

### Web application
The application is written with React framework on frontend and Flask on backend. The deployment is done using docker. 