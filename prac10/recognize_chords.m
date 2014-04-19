function [Labels,Liks] = recognize_chords(Chroma, Models, Transitions, Priors)
% [Labels,Liks] = recognize_chords(Chroma, Models, Transitions)
%     Take a 12xN array of chroma features Chroma, an array of 
%     Gaussian models Models(i).mean and Models(i).sigma
%     (covariance), and a transition matrix Transitions 
%     and calculate the most likely (Viterbi) label sequence, 
%     returned in Labels.  The likelihoods of each model for each
%     frame are returned in Liks.
% 2010-04-07 Dan Ellis dpwe@ee.columbia.edu after doChordID.m

[nftrdims,nframes] = size(Chroma);
nmodels = length(Models);  % num models

Liks = zeros(nmodels,nframes);
% evaluate each frame under all models
for j = 1:nmodels; 
  Liks(j,:) = gaussian_prob(Chroma, Models(j).mean, Models(j).sigma); 
end

% Evaluate viterbi path
Labels = viterbi_path(Priors,Transitions,Liks);
% Make the labels be 0..24 
Labels = Labels - 1;

