# instagram
Automated process of determining followers and following of users Instagram account.

Makes use of Selenium to create a Chrome Web Driver instance to be used to sign-in to Instagram, and create lists of instances representing the users followers and following. Using Pandas, these lists are then used to create Dataframes to provide a comprehensible output.

Current output of the program is only a list of individuals that the user follows, but do not follow the user back.

TODO:
 - Allow user to also search by public accounts, rather than having to sign in.
 - Create unfollow all function
 - Create follow all function
 - Find more specific CLASS_NAME attribute for pulling instances representing the users followers and following to make process more efficient 
