% ASP query example for grasp

#const target="ENVO_00002007".

% is interesting any object related to the target
interesting(Object):- triplet(Object,_,target).

% find some interesting definitions to send to your students
to_learn(Object,Definition):- triplet(Object,"IAO_0000115",Definition) ; interesting(Object).

% next lines defines the output of the query (not necessary most of the time)
#show.
%#show interesting/1.
#show to_learn/2.
