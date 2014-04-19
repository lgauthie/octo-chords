function Chroma = labels_to_chroma(Labels)
% Chroma = labels_to_chroma(Labels)
%    Generate a "canonical" chroma feature sequence based on
%    labels.  Assume Labels(i) is 0..24, with 0 = no chord, 
%    1 = Cmajor, 2 = C#major ... 13 = Cminor .. 24 = Bminor.
%    Corresponding columns of Chroma are simple triad for those
%    chords.
% 2010-04-07 Dan Ellis dpwe@ee.columbia.edu

nlab = length(Labels);
nchr = 12;

Chroma = zeros(nchr,nlab);

for i = 1:nlab
  
  lab = Labels(i);
  if lab > 12
    % minor chord
    Chroma(1+mod(lab-13+[0 3 7],12),i) = 1;
  elseif lab > 0
    % major chord
    Chroma(1+mod(lab-1+[0 4 7],12),i) = 1;
  end

end
