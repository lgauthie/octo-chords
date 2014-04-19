function X = synthesize_chroma(Chroma,Times,SR)
% X = synthesize_chroma(Chroma,Times,SR,npks)
%   Resynthesize a chroma feature vector to audio
%   Chroma is 12 rows x some number of columns, one per beat
%   Times is vector of beat times
%   SR is the sampling rate of the output waveform
%   X is returned as a 12 semitone-spaced Shepard tones modulated
%   by Chroma.
% 2010-04-07 dpwe@ee.columbia.edu after chromsynth2.m

if nargin < 2; Times = 0.5; end % 120 bpm
if nargin < 3; SR = 22050; end

[nchr,nbts] = size(Chroma);

if length(Times) == 1   % just period, not times
  Times = cumsum(Times * ones(1,nbts));
end

% Select only local maxima, with wrapping around edges
Xm = (Chroma > Chroma([2:nchr,1],:)) & (Chroma >= Chroma([nchr,1:nchr-1],:));
Chroma = Xm.*Chroma;

if length(Times) < (nbts+1)   % +1 to have end time of final note(s) ?
  medbt = median(diff(Times));
  Times = [Times, Times(end)+medbt*[1:((nbts+1)-length(Times))]];
end

% crossfade overlap time
dt = 0.01;
dtsamp = round(dt*SR);

% Generate 12 basic shepard tones
dur = max(diff([0,Times])); % max duration
dursamp = round(dur*SR);
nchr = 12;
octs = 10;
basefrq = 27.5*(2^(3/12));  % A1+3 semis = C2;

tones = zeros(nchr, dursamp + 2*dtsamp + 1);
tt = [0:(size(tones,2)-1)]/SR;

% what bin is the center freq?
f_ctr = 880;
f_sd = 1;
f_bins = basefrq*2.^([0:(nchr*octs - 1)]/nchr);
f_dist = log(f_bins/f_ctr)/log(2)/f_sd;  
% Gaussian weighting centered of f_ctr, with f_sd
%if (dowt)
  f_wts = exp(-0.5*f_dist.^2);
%else
%  % flat weights
%  f_wts = ones(1,length(f_dist));
%end
% Sum up sinusoids
for i = 1:nchr
  for j = 1:octs
    bin = nchr*(j-1) + i;
    omega = 2* pi * f_bins(bin);
    tones(i,:) = tones(i,:)+f_wts(bin)*sin(omega*tt);
  end
end

% resynth
X = zeros(1,round(max(Times)*SR));

ee = round(SR*Times(1));
for b = 1:nbts-1
  ss = ee+1;
  ee = round(SR * Times(b+1));
  twin = 0.5*(1-cos([0:dtsamp-1]/(dtsamp-1)*pi));
  twin = [twin,ones(1,ee-ss+1),fliplr(twin)];
  sss = ss - dtsamp;
  eee = ee + dtsamp;
  if eee > length(X)
    twin = twin(1:end-(eee-length(X)));
    eee = length(X);
  end
  if sss < 1
    twin = twin((2-sss):end);
    sss = 1;
  end

  ll = 1+eee-sss;
  dd = zeros(1,ll);
  for i = 1:nchr
    if Chroma(i,b)>0
      dd = dd + Chroma(i,b)*tones(i,1:ll);
    end
  end
  X(sss:eee) = X(sss:eee) + twin .* dd;
  
end

