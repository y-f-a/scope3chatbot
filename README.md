# ClimateChoice Scope 3 Chatbot 

This [Streamlit](https://streamlit.io/) app is designed to help you navigate the latest [GHG Protocol](https://ghgprotocol.org/) Scope 3 documentation. 

The app uses [OpenAI's](https://openai.com/) Large Language Models (LLMs) with [Llamaindex](https://www.llamaindex.ai/) to enable a Retrieval-Augmented Generation (RAG) approach. RAG combines the use of generative models with targeted retrieval of relevant information from documents and data sources to produce more accurate and context-aware responses. Learn more about Llamaindex's approach to RAG [here](https://docs.llamaindex.ai/en/stable/getting_started/concepts/).

Simply put, this lets you ‘chat’ with complex documents using a software assistant, guiding you through the content and answering any questions you may have.

# Source Data

The documents used to form the foundational data for the RAG approach have been taken solely from the [GHG Protocol](https://ghgprotocol.org/). They cover the official guidance as well as the recent discussion findings from recent consultations:

- [Corporate Value Chain Accounting Reporting Standard E-Reader Version (156 pages)](https://ghgprotocol.org/sites/default/files/standards/Corporate-Value-Chain-Accounting-Reporing-Standard-EReader_041613_0.pdf)
- [Technical Guidance for Calculating Scope 3 Emissions - Supplement to the Corporate Value Chain (Scope 3) (182 pages)](https://ghgprotocol.org/sites/default/files/2023-03/Scope3_Calculation_Guidance_0%5B1%5D.pdf)
- [Scope 3 Frequently Asked Questions (22 pages)](https://ghgprotocol.org/sites/default/files/2022-12/Scope%203%20Detailed%20FAQ.pdf)
- [Scope 3 Survey Final Summary Report (93 pages)](https://ghgprotocol.org/sites/default/files/2024-06/Scope%203%20Survey%20Summary%20-%20Final%20%281%29.pdf)
- [Scope 3 Final Proposal Summary (26 pages)](https://ghgprotocol.org/sites/default/files/2024-06/Scope%203%20Proposals%20Summary%20-%20Final_0.pdf)
	
These documents were processed using the [Azure Document Intelligence](https://azure.microsoft.com/en-gb/products/ai-services/ai-document-intelligence) service to conver them into markdown equivalents, which tends to produce the best results with OpenAI's model in this domain.

# Notes

To use this app, you will need to familiarize yourself with how a Streamlit app operates. The app is configured to utilize LLMs hosted on Azure, so be sure to consider the associated costs for your specific use cases if you plan to run it yourself.

Contributions and suggestions are very welcome. This app was brought to you by the [ClimateChoice](https://theclimatechoice.com/en/).

