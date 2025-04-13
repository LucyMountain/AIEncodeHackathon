Encode AI Hackathon  

Defi-Investment Types 

Group Project – Koyna Chakravorty, Lucy Mountain, Hamim Al Hussain, Yin Mui Tai, Gokul Krishna 

Project Title: DeFi Investment Recommendation Assistant 

 

​​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​​ 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

1 Analysis 

1.1 Required Specification 

1.1.1 Portia ai 

Build complex and controllable AI agents on Portia AI 

Portia AI is an open-source SDK that wants to stand out because it helps AI agents pre-express their planned response to a prompt, share their progress during execution, and solicit human input under defined conditions. 

 

1.1.2 Solana - Defi 

To build an AI-driven blockchain solution  

DeFi refers to a system of financial applications built on blockchain networks, aiming to recreate and improve upon traditional financial systems without centralized intermediaries. On Solana, DeFi has flourished due to the platform's high performance, scalability, and low transaction costs, making it a preferred choice for developers and users alike. 

 

 

1.2 Choosing Specification 

At the outset, our team explored multiple bounty options without a clear direction. After some discussion, we narrowed down our interest to two key areas: Portia AI and Solana DeFi. 

Upon further investigation, we observed that Portia AI had relatively limited documentation and learning resources, with only a few tutorial videos available. In contrast, Solana and its DeFi ecosystem had abundant documentation, community examples, and educational content, which significantly lowered the learning curve. 

Given our project timeline and the need for rapid prototyping, we chose to work with the Solana DeFi bounty. We believe its ecosystem provides a more practical foundation for developing a complete, data-driven solution using existing tools and APIs. 

 

1.3 Plan 

Our goal was to build a web-based AI assistant that leverages DeFi data to provide personalized investment advice based on a user’s salary, lifestyle, and current market opportunities. To structure our work efficiently, we distributed tasks among group members based on areas of focus: 

 

 

 

 

 

We also planned to utilize the following technologies and libraries: 

 

By combining these tools, we aimed to create a functional, interactive prototype that not only showcases the technical feasibility of our idea but also delivers meaningful utility to everyday users exploring DeFi. 

 

 

 

1.4 Research  

1.4.1Existing solutions 

We looked into current DeFi tools to understand what exists in the ecosystem and how our solution could improve on them. 

DeFiLlama is a widely used DeFi TVL aggregator. It provides transparent and ad-free data tracking across chains, focusing on rankings and raw TVL statistics. However, it lacks actionable insights or personalization, especially for users unfamiliar with DeFi metrics. 

Raydium is a Solana-based DeFi platform combining an automated market maker (AMM) with an on-chain order book. While it provides liquidity and trading infrastructure, it does not offer personalized investment recommendations or educational guidance for users. 

Unlike these platforms, our solution goes a step further by providing: 

AI-powered personalized investment suggestions 
Based on user-specific inputs (e.g., income, living costs), our platform tailors DeFi opportunities to each individual, not just showing generic yield data. 

Categorization by Investment Types 
Instead of a single TVL leaderboard, we group opportunities into types (e.g., stablecoin yield, staking, liquid staking, etc.), allowing users to understand risk/reward trade-offs in a more structured way. 

Transparency and Explainability 
Most auto-yield aggregators function as black boxes. In contrast, our system explains the logic behind each recommendation (e.g., Sharpe ratio, protocol risk score), giving users confidence and clarity in their investment decisions. 

 

1.4.2 Research conclusion 

Our research showed a significant gap in the market: tools that can make DeFi approachable for everyday users who are not crypto-native. By combining accessible UX with personalized, explainable recommendations, our project addresses this need directly. 

 

1.5 Solution 

1.5.1 Essential features 

To address this gap, we focused on building a functional, interactive website with the following core features: 

Backend Logic in Python 
 Our backend processes user input (e.g., salary) and combines it with on-chain DeFi pool data to generate personalized investment suggestions. 

Interactive Frontend with CSS and Visualizations 
 The frontend is built to be intuitive and informative to help users better understand pool performance, risk scores, and potential returns. 

 

Educational and Transparent UI 
 We plan to include animation or slideshows that walk the user through how the system works and what each metric means — lowering the barrier for new DeFi users. 

 

We also wanted to allow the user to easily grasp the idea of how our website works this would be by implementing graphs for a better visual understanding or maybe even animations which go through a series of slides which explains and decomposes our website's goal 

 

 

1.5.2 Limitations 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

1.6 Success criteria 

 

Success criteria 

Description 

Expected outcome 

Working webpage 

The website must be able to run successfully without critical errors, integrating both frontend and backend components. 

A stable, functioning site accessible via browser, Python backend communicates with HTML/CSS frontend. 

GitHub Collaboration 

Maintain a shared GitHub repository to enable collaborative development and version control. 

All team members contribute via Git, code changes are tracked and synchronized. 

Backend Integration 

Ensure Python backend processes inputs from the user and sends results back to the frontend in real time. 

Backend functions are triggered via user actions, and the output is dynamically rendered in the frontend. 

API and Library Utilization 

Use external libraries and APIs for data access, processing, and visualization. 

No compatibility or dependency errors; APIs return and display expected data. 

Data Handling and Automation 

We plan to add a csv file and manipulate it so that it is specialized for each specific user 

We should be able to manipulate the statistical data within the file and use this to help automate financial advice  

Implement calculations 

Develop functions which calculate the credible highest ROI which should be specialized for each user 

We should be able to use the data from both the api, csv file and user input to manipulate data and recommend the optimal financial advice to the user 

 

 

 

 

2 Design and Implementation 

2.1 Decomposition 

From the same document which our group gained an understanding of what we wanted to build we broke each major part of the code into parts and decomposed the problem. 

Web dev: 

Backend 1st stage (receiving user inputs outputting suitable solutions): 

 

 

 

 

 

 

 

Backend 2nd  stage(fetching and using data via the api): 

 

Backend 3rd stage (): 

 

 

 

 

 

 

Backend stage 4: 
 

The original plan for data Acquisition and handling was to fetch cost of living data using the Numbeo API and obtain financial data for stocks and cryptocurrencies using yfinance. 

Current implementation: We have replaced the Numbeo API with a .csv file from Kaggle for costs of living data to simplify data retrieval and avoid external API dependencies. Shifted focus exclusively to Solana-based DeFi protocols, eliminating the need for stock and general cryptocurrency data. 

 

Backend stage 5: 
 

Original plan for core functionality and logic: calculate disposable income by subtracting annual rent from the user’s salary. Recommend investments based on disposable income levels, suggesting a mix of conservative and riskier assets. 

Current implementation: Calculate monthly disposable income by subtracting city-specific living costs from the user's salary. Recommend Solana-based DeFi protocols based on user-defined risk tolerance and preferred investment types. Compute estimated Return on Investment (ROI) using current and historical TVL data. 

 

Backend stage 6:  

 

Original plan for UI: utilise stream lit to create a UI with input fields for city, salary, and investment timeline, along with buttons to trigger analysis. 

Current implementation: The UI development now uses HTML and CSS instead of stream lit. 

 

 

 

 

2.2 System structure 

2.2.1 Visualization 

 

 

 

3 Testing 

3.1 Test data 

Method testing 

Variable testing 

Expected outcome 

get_all_protocols() 

 

Response 

No exception 

 

response.raise_for_status() 

 

No exception 

def get_batch_historical_prices(coins_dict, search_width): 

 

 

 

 

 

 

 

 

 

 

 

3.2 Iterations  

3.2.1 Iteration 1 –backend stage 1 

- 

3.2.2 Iteration 2 - 

- 

 

3.2.3 Iteration 3 - 

- 

 

3.2.4 Iteration 4 - 

- 

 

3.3 Post-development testing 

 

 

 

4 Evaluation 

4.1 Progress on success criteria 

Success criteria 

Description 

Expected outcome 

Actual outcome (not met, partially complete or complete) 

Working webpage: 

The website must be able to run successfully without critical errors, integrating both frontend and backend components. 

A stable, functioning site accessible via browser, Python backend communicates with HTML/CSS frontend. 

complete 

GitHub Collaboration: 

Maintain a shared GitHub repository to enable collaborative development and version control. 

All team members contribute via Git, code changes are tracked and synchronized. 

complete 

Backend Integration: 

Ensure Python backend processes inputs from the user and sends results back to the frontend in real time. 

Backend functions are triggered via user actions, and the output is dynamically rendered in the frontend. 

complete 

API and Library Utilization: 

Use external libraries and APIs for data access, processing, and visualization. 

No compatibility or dependency errors; APIs return and display expected data. 

complete 

Data Handling and Automation: 

We plan to add a csv file and manipulate it so that it is specialized for each specific user 

We should be able to manipulate the statistical data within the file and use this to help automate financial advice  

Partially complete 

Implement calculations: 

Develop functions which calculate the credible highest ROI which should be specialized for each user 

We should be able to use the data from both the api, csv file and user input to manipulate data and recommend the optimal financial advice to the user 

 

Partially complete 

 

 

4.1.1 Improvements 

 

Backend: 

1. Data acquisition- 

Implemented a function to update the cost-of-living dictionary from the CSV file, ensuring flexibility in data management. 

 Utilised the DeFiLlama API to fetch real-time data on Solana protocols, including current and historical Total Value Locked (TVL). 

 

2. Core functionality logic- 

Introduced a risk assessment mechanism categorizing protocols into Low, Medium, or High risk based on TVL thresholds. 

Mapped specific protocols to investment categories for more tailored recommendations 

 

3. UI and web design- 

Added selected options for risk tolerance and investment types to provide more personalised recommendations. 

Include explanations of different investment types to educate users. 

 

Frontend: 

Input sanitisation and validation: 

 

Enhanced security- 

By validating and sanitising user inputs, the application mitigates risks associated with malicious data entry, such as code injection attacks. This practice is fundamental in preventing vulnerabilities like SQL injection and cross-site scripting (XSS), which can compromise user data and application integrity. 

 

Improved data integrity- 

Ensuring that only properly formatted and expected data enters the system maintains the consistency and reliability of the application’s data. This prevents issues that could arise from malformed or unexpected input, safeguarding the application's functionality. 

 

Better user experience- 

Implementing input validation provides immediate feedback to users, guiding them to enter correct information. This reduces frustration, decreases the likelihood of errors, and enhances ovrall user satisfaction. 

Regulatory Compliance-  

Proper input handling aligns with data protection regulations and standards, such as GDPR and HIPAA, by ensuring that user data is processed securely and responsibly. 

Reduced maintenance and debugging- 

By catching invalid inpts early, the application minimises the occurrence of bugs and errors downstream, simplifying maintenance and reducing the time spent on debugging. 

 

 

 

4.2 Maintenance and limitation evaluation 

Throughout the development of our project, we encountered a number of challenges—both technical and organizational—that shaped our final outcome and informed valuable lessons for the future. 

First, from a team perspective, most of our members had limited prior experience with hackathons, and for several, this was their very first. As a result, we experienced a steep learning curve not only in mastering new technologies, but also in learning how to work together effectively under time pressure. This was further complicated by the unexpected departure of two original teammates midway through the event, which required us to reorganize roles and redistribute tasks during critical phases of the hackathon. As a result, some features were deprioritized, and our development pace was occasionally disrupted as we adapted to the new team structure. 

Despite these challenges, we ensured that our codebase remained well-maintained. We consistently documented our progress on GitHub, providing clear commit messages and maintaining version control to facilitate collaboration. Code was annotated to support the next developer, ensuring a smoother transition for any ongoing work. 

On the technical side, a key limitation in the current version of the platform is the access to real-time on-chain data. While the current version of our platform uses publicly available aggregated data sources, we recognize that the next phase of the platform's growth requires more advanced data integration. Specifically, Solana protocols will continue to serve as the foundational source for on-chain DeFi data, enabling us to offer accurate and timely insights into the decentralized finance ecosystem. However, to enhance the level of personalization and real-time adaptability of our recommendations, integrating paid on-chain data APIs will be essential. 

As we look to scale the platform, AI-driven features will be at the forefront of providing users with intelligent, tailored suggestions. By leveraging portal AI, we aim to continuously improve our recommendations based on user behavior, preferences, and risk tolerance. With more time, we would have integrated AI to not only process DeFi protocol data but also guide users through interactive experiences, helping them make well-informed investment decisions with greater confidence. Through this, we hope to offer a platform that doesn't just present a list of opportunities, but actively assists in optimizing users’ portfolios based on their personal financial goals. 

 

 

 

 

 

 

 

 
