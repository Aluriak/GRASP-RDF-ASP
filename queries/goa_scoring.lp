% Scoring on goa data.
% Each protein is scored, according to the number of annotation it have.
% only the best annotated proteins are outputed.


% a protein is an object annotated by GOA
protein(X):- entry(X,_,_).

% choose ten proteins.
1 { choosen(X): protein(X) } 3.

% the score is the number of entry where the choosen protein is the object.
score(Protein,Score):- Score={entry(Protein,_,_)} ; choosen(Protein).

% compute the total score of the choosen proteins.
total_score(T):- T=#sum{S:score(X,S), choosen(X)}.

% Maximize the score of the ten choosen proteins.
#maximize{S:total_score(S)}.


% outputs.
#show.
#show choosen/1.
#show score/2.
#show total_score/1.
