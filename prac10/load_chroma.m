function [Chroma,Times] = load_chroma(Track)
% [Chroma,Times] = load_chroma(Track)
%     Read in features for data items defined by a track ID string Track.
%     Chroma returns the 12xN matrix of chroma features, one per beat.
%     Times returns the start times of each beat.
% 2010-04-07 Dan Ellis dpwe@ee.columbia.edu after loadftrs_mirex.m

% Common filename prefix
fn = fullfile('data','chroma', Track);
Data = load(fn);

Times = Data.bts;
Chroma = Data.F;
% Normalize chroma to have maximum value 1 in each column
%Chroma = Chroma.^.25;
MaxVals = max(Chroma);
Chroma = Chroma.*repmat(1./MaxVals, size(Chroma,1), 1);
