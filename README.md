# Data Science CS109 HW4:Do we really need Chocolate Recommendations?

###Collaborative Filtering systems

In this homework, you will create a recommendation system for **restaurants** using [collaborative filtering](http://en.wikipedia.org/wiki/Collaborative_filtering) (CF). The general structure of a recommendation system is that there are users and there are items. Users express explicit or implicit preferences towards certain items. CF thus relies on users' past behavior.

There are two primary approaches to CF: neighboorhood and latent factor model. The former is concerned with computing the relationships between items or between users. In the latter approach you have a model of hidden factors through which users and items are transformed to the same space. For example, if you are rating movies we may transform items into genre factors, and users into their preference for a particular genre.

Factor models generally lead to more accurate recommenders. One of the reasons for this is the sparsity of the item-user matrix. Most users tend to rate barely one or two items. Latent factor models are more expressive, and fit fewer parameters. However, neighborhood models are more prevalent, as they have an intuitive aspect that appeals to users(if you liked this you will like that) and online(a new preference can be incorporated very quickly).

Most recommenders today combine neighboorhood CF with model based CF, and SVD based matrix factorization approaches.

To see the example of a simple beer recommender, go [here](http://nbviewer.ipython.org/20a18d52c539b87de2af). This homework is inspired by the one there but we go after food instead, and go deeper into the problem of making recommendations.


### User and Item based approaches

Original approaches to neighborhood based CF used user-user models. By this we mean that rating estimates are made from recorded ratings of like minded users. However, since most users tend to rate very few items, this is usually a losing proposition for explicit-rating based recommenders. Thus, most neighborhood based systems such as Amazon these days rely on item-item approaches. In these methods, a rating is estimated by other ratings made by the user on "similar" or "nearby" items: we have a K-Nearest-Neighbors algorithm, in effect.


###Outline of this Homework

The outline of this homework is as follows:

1. Create a database of item-item similarities. Use this to implement a neighborhood-based CF recommender that can answer simple questions like "give me more restaurants like this one". This part of the homework assumes that the similaties calculated make good "global recommendations".

2. In the second part, we go one step further and attempt to predict the rating that a user will give an item they have not seen before. This requires that we find the restaurants that *this* user would rate as similar (not just those which are globally similar). 

3. In the third part, we implement a factor-based CF recommender using a Bayesian model. While quite a bit more complex, this allows us to pool information both about similar users and about similar restaurants.

5. We will scale up our system by creating a recommender on the lines of Q1 and Q2 that works on the entire data set. We will use the map-reduce paradigm to split the computation over multiple machines.


You will start simply, by working on a subset of the restaurant data before generalizing to the entire data set in Problem 4. The complete data set has 150,000 reviews, but we shall start with just about 7000. You will create this  smaller set by taking all the users who had rated more than 60 restaurants, and all the businesses which had greater than 150 reviews from the larger data set. This is not a random set: indeed we use it as it a computationally tractable set that is a bit less sparse than the entire data set.
