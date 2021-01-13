# Trav4me
A basic prototype of a Transportation Model - Post pandemic. 

The inspiration for this prototype is based on this paper - https://arxiv.org/pdf/2012.15749.pdf

The paper explains the concept of considering cost, latency, and an additional parameter - Risk of Infection(ROI) while recommending the most feasible modes of transport. It also explains how to use a preference distribution model and active querying to offer a more personalized experience.   

Risk of infection is calculated using parameters such as - capacity of the road, flow of population in trains, buses and footpaths. The math involved in calculating the risk of infection, creating and solving the optimization problem and creating a preference distribution model is clearly explained in the paper.  

This build of the prototype is still a work in progress. The data that should have been obtained using the Google Maps API and the Ola/Uber API has been hard coded.
Also, predictions of population density in modes of public transport like trains and buses have been hard coded. As an upcoming improvement, the prediction would be done using a trained machine learning model, wherein the training data used would be provided by the BMTC(local authority of Buses), IRCTC(Authority on Railways), Ola/Uber(or others) as when the data is made available. Also, the math involved in the paper needs to be implemented, after careful thought , in the building of the prototype.   

In my implementation, I have considered 6 different modes of transport - 
1. Railways,
2. Buses,
3. Private Vehicle - 4 wheeler,
4. Private Vehicle - 3 Wheeler,
5. Cabs/Auto and
6. Walking. 
