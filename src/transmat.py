import sys
import pickle

import numpy as np
import numpy.matlib as ml

from sklearn.hmm import GaussianHMM

def main():
    """
    First ARG: list of training files
    Second ARG: save name for model
    """
    file1 = sys.argv[1]
    outname = sys.argv[2]
    file_list = [f[0:-1] for f in open(file1,'r')]
    models, transitions, priors = calc_transmat(file_list)
    hmm = GaussianHMM(
        transitions.shape[0],
        "full",
        startprob=priors,
        transmat=transitions,
    )
    hmm.means_ = np.transpose(models['mean'])
    hmm.covars_ = models['sigma']
    pickle.dump(hmm, open(outname, "wb"))

def calc_transmat(file_list):
    features, labels = load_feats_labels(file_list)
    globalmean = np.array(map(np.mean, features))
    globalcov = np.cov(features)
    pairs = zip(labels, np.transpose(features))
    models = {'mean':np.array([]), 'sigma':np.array([])}

    # Create individual models for each chord
    states = get_labels()
    for i,label in enumerate(states):
        examples = filter(lambda (x,_): x == label, pairs)
        if examples:
            [_, feats] = zip(*examples)
            models['mean'] = np.append(models['mean'],
                                       np.array(map(np.mean, np.transpose(feats))))
            models['sigma'] = np.append(models['sigma'],
                                        np.cov(feats, rowvar=0))
        else:
            models['mean'] = np.append(models['mean'],
                                       globalmean)
            models['sigma'] = np.append(models['sigma'],
                                        globalcov)
    models['mean'] = models['mean'].reshape(12,models['mean'].size/12)
    models['sigma'] = models['sigma'].reshape(models['sigma'].size/(12*12),12,12)

    n = len(states)
    transitions = np.zeros(shape=(n,n))
    trans = zip(labels[0:-1], labels[1:])
    for (i, ikey) in enumerate(states):
        for (j, jkey) in enumerate(states):
            # Add one so there is no zero probabilities
            transitions[i,j] = 1 + sum([1 for (f, s) in trans
                                        if f == ikey and s == jkey])
    priors = np.sum(transitions, 1)
    transitions = np.divide(
        transitions,
        ml.repeat(priors, transitions.shape[1]).reshape(transitions.shape)
    )
    priors = priors/np.sum(priors)
    return (models, transitions, priors)

def get_labels():
    """ Generate All possible chord labels """
    notes = [
        'A',  'B',  'C',  'D',  'E',  'F',  'G',
        'A#', 'B#', 'C#', 'D#', 'E#', 'F#', 'G#',
        'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'Fb', 'Gb',
    ]
    quals = ['maj', 'min', 'aug', 'dim', 'sus2', 'sus4']
    labels = [note + ':' + qual for note in notes for qual in quals]
    labels.extend(['X', 'N'])
    return labels

_labels = get_labels()
def int2label(i):
    return _labels[i]

def load_feats_labels(file_list):
    """ Read all chord labels from a list of files """
    features = np.array([])
    labels = np.array([])
    for path in file_list:
        with open(path, 'r') as f:
            contents = np.array(
                [l[0:-1].split(',') for l in f if not l[0] in ['%', '@', '\n']]
            )
            labels = np.append(
                labels,
                np.array([label for label in contents[:,-1]])
            )
            features = np.append(
                features,
                np.array([map(float, feat) for feat in contents[:,0:-1]])
            )
    features = features.reshape(12,np.size(features)/12)
    return (features, labels)

if __name__=="__main__":
    main()