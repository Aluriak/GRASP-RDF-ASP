% Scoring on goa data.
% Each protein is scored, according to the number of annotation it have.
% only the best annotated proteins are outputed.


% a protein is an object annotated by GOA
protein(X):- triplet(X,_,_).
protein(X):- triplet(_,_,X).


% choose ten proteins.
10 { choosen(X): protein(X) } 10.

% the score is the number of triplet where the choosen protein is the object.
score(Protein,Score):- Score={triplet(Protein,_,_)} ; choosen(Protein).

% compute the total score of the choosen proteins.
total_score(T):- T=#sum{S:score(X,S), choosen(X)}.

% Maximize the score of the ten choosen proteins.
#maximize{S:total_score(S)}.


% outputs.
#show.
#show choosen/1.
#show score(P,S): choosen(P), score(P,S).
#show total_score/1.
