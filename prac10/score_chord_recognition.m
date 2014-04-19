function [S,C] = score_chord_recognition(H,R)
% [S,C] = score_chord_recognition(H,R)
%     Score chord recognition systems.  
%     H is the hypothesized (system output), R is the reference
%     (truth) data. Both are vectors of chord labels (0..24).
%     H and R must be the same length
%     S returns as the overall accuracy (between 0 and 1); 
%     C returns a confusion matrix (e.g. 25 x 25)
% 2010-04-07 Dan Ellis dpwe@ee.columbia.edu after score_chord_id.m

npmodels = 2;
nchroma = 12;
nlabels = npmodels * nchroma + 1;

C = zeros(nlabels, nlabels);

for i = 1:length(H)
  C(R(i)+1,H(i)+1) =  C(R(i)+1,H(i)+1) + 1;
end

S = sum(diag(C)) / sum(sum(C));