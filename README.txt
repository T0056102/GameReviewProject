#	1. Display "not clicked" thumb up & thumb down next to the ratings. 										
2. Display zero instead of "None".
#	3. Add primary key (username,articleid) to articlerating table.
4. Add new route for clicking up thumb for user/article, and corresponding route for clicking down thumb.
#		These two routes should only accept the POST method.
#		The routes should be something like "/ArticlesAdd/<articleID>/<username>" (see route "/Articles/<articleID>" for how that works).
	They update the database with the new rating situation for the username & article id.
	They should redirect to a http status code 403 (forbidden) if the user is not logged in.
	Then re-display the article with the new scores i.e. redirect back to "/Articles/<articleID>" route.
#	5. Add anchor <A> round the thumbs with href of the 2 new routes you added at 4.
#		Only add the <A> tags if the user is logged in.
6. Change "/Articles/<articleID>" route so that green or red thumbs are displayed if the user has already done a review.
7. Update createDatabase to include creation of articlerating database and the primary key index for it.
	