function [S,C] = test_chord_models(TestFileList, Models, Transitions, Priors)
% [S,C] = test_chord_models(TestFileList, Models, Transitions, Priors)
%     Test chord recognizer on multiple tracks
%     TestFileList is a cell array containing track ID strings for
%     the test file.
%     Models, Transitions, Priors define the chord recognition HMM
%     from train_chord_models.
%     S returns as the overall accuracy (between 0 and 1); 
%     C returns a confusion matrix (e.g. 25 x 25)
% 2010-04-07 Dan Ellis dpwe@ee.columbia.edu after score_chord_id.m

% Total # labels = Total # models = {major,minor} x {all chroma} + NOCHORD
nchroma = 12;
nlabels = 2 * nchroma + 1;
NOCHORD = 0;

% Initialize confusion matrix
C = zeros(nlabels, nlabels);

% Run recognition on each file individually
nTestFiles = length(TestFileList);
for i = 1:nTestFiles
  Chroma = load_chroma(TestFileList{i});
  TrueLabels = load_labels(TestFileList{i});
  HypLabels = recognize_chords(Chroma, Models, Transitions, Priors);
  [s,c] = score_chord_recognition(HypLabels, TrueLabels);
  C = C + c;  % cumulate actual seconds spent in each state
end

% Actual accuracy %.  
% Exclude regions where both streams report No Chord (e.g. lead
% in/lead out)

XX = C(NOCHORD+1, NOCHORD+1);

S = (sum(diag(C))-XX) / (sum(C(:))-XX);

disp(['Overall recognition accuracy = ',sprintf('%.1f',100*S),'%']);
