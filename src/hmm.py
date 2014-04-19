TrainFileList = textread('trainfilelist.txt','%s');

# Load beat-synchronous chroma for "Let It Be" - item 135
[Chroma,Times] = load_chroma(TrainFileList{135});

# Train Gaussian models for each chord from whole training set
[Models,Transitions,Priors] = train_chord_models(TrainFileList);

# Look at the means of the 25 learned models (nochord + 12 major + 12 minor)
for i = 1:25; MM(:,i) = Models(i).mean(TRANSPOSE); end

# Plot chroma vectors
imagesc(MM)
chromlabels = 'C|C#|D|D#|E|F|F#|G|G#|A|A#|B';
set(gca, 'YTick', 1:12);
set(gca, 'YTickLabel', chromlabels);
keylabels = '-|C|C#|D|D#|E|F|F#|G|G#|A|A#|B|c|c#|d|d#|e|f|f#|g|g#|a|a#|b';
set(gca, 'XTick', 1:25);
set(gca, 'XTickLabel', keylabels);

# Try recognizing chords
[HypChords, LHoods] = recognize_chords(Chroma,Models,Transitions,Priors);

# We can look at the best 'Viterbi' path overlaid on the per-frame log likelihoods
imagesc(max(-10,log10(LHoods)));
colormap(1-gray)
colorbar
hold on; plot(HypChords+1,'-r'); hold off

#Look just at the first hundred beats
axis([0 100 0.5 25.5])
xlabel('time / beats');
ylabel('chord');
set(gca,'YTick',1:25);
set(gca,'YTickLabel',keylabels);

#Compare the 'Viterbi HMM' path to the simple most-likely model for each frame
[Val,Idx] = max(LHoods);
hold on; plot(Idx, 'og'); hold off

#The HMM transition matrix makes it more likely to stay in any given state, 
#thus it smooths the chord sequence (eliminates single-frame chords)

#Evaluate accuracy compared to ground-truth
TrueChords = load_labels(TrainFileList{135});

#Add the true labels to the plot
hold on; plot(TrueChords+1, '.y'); hold off
legend('Viterbi','Best','True')

# HypChords and TrueChords are simple vectors of labels in range 0..24.
#What is the average accuracy for this track?
mean(HypChords==TrueChords)

#71.5% - pretty good!
# For reference, the best per-frame model, without the HMM, gives
mean(Idx-1 == TrueChords)  % subtract 1 to convert indices 1..25 into chords 0..24
#44.9% - nowhere near as good

# To get the full confusion matrix (rows=true, cols=recognized as):
[S,C] = score_chord_recognition(HypChords,TrueChords);
imagesc(C);
set(gca,'XTick',1:25);
set(gca,'XTickLabel',keylabels);
set(gca,'YTick',1:25);
set(gca,'YTickLabel',keylabels);
# Most common confusion is F being recognized as C.

# What do the true chords sound like when rendered as Shepard tones?
LabelChroma = labels_to_chroma(TrueChords);
#.. creates a simple chroma array with canonical triads for each chord
X2 = synthesize_chroma(LabelChroma,Times,SR);
soundsc(X2(1:20*SR),SR)

# Compare "target" chroma, actual chroma, and both true and hypothesized labels
subplot(311)
imagesc(LabelChroma);
axis xy
set(gca, 'YTick', [1 3 5 8 10 12]'); set(gca, 'YTickLabel', 'C|D|E|G|A|B');
subplot(312)
imagesc(Chroma);
axis xy
set(gca, 'YTick', [1 3 5 8 10 12]'); set(gca, 'YTickLabel', 'C|D|E|G|A|B');
subplot(313)
plot(1:length(TrueChords),TrueChords,'o',1:length(HypChords),HypChords,'.r')
legend('True','Hyp')
set(gca,'YTick',[1 3 5 8 10 13 15 17 20 22]); set(gca,'YTickLabel','C|D|E|G|A|c|d|e|g|a');
axis([0 length(TrueChords) 0 25])
colormap hot
#This gives the picture above

#Evaluate recognition over entire test set
TestFileList = textread('testfilelist.txt','%s');
[S,C] = test_chord_models(TestFileList,Models,Transitions,Priors);
#Overall recognition accuracy = 57.7%
