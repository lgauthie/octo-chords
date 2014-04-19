function [Labels,Times] = load_labels(Track)
% [Chroma,Times] = load_labels(Track)
%     Read in labels for data items defined by a track ID string Track.
%     Labels returns an N-element vector of integer labels (0..24)
%     for each beat.
%     Times returns the start times of each beat.
% 2010-04-07 Dan Ellis dpwe@ee.columbia.edu after loadftrs_mirex.m

% Common filename prefix
fn = fullfile('data','labels', Track);
Data = load(fn);

Times = Data.bts;
% Labels are written as a column, return as a row
Labels = Data.L';
