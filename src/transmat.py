import sys

import numpy as np
import numpy.matlib as ml

from sklearn.hmm import GaussianHMM
from collections import defaultdict

def main():
    file1 = sys.argv[1]
    file_list = [f[0:-1] for f in open(file1,'r')]
    models, transitions, priors = calc_transmat(file_list)
    hmm = GaussianHMM(
        n_components=transitions.shape[0],
        transmat=transitions,
        startprob=priors,
    )
    import ipdb; ipdb.set_trace()

def calc_transmat(file_list):
    features, labels = load_feats_labels(file_list)
    globalmean = np.array(map(np.mean, features))
    globalcov = np.cov(features)
    pairs = zip(labels, np.transpose(features))
    models = {'mean':globalmean, 'sigma':globalcov}

    # Create individual models for each chord
    states = get_labels()
    for label in states:
        examples = filter(lambda (x,_): x == label, pairs)
        if examples:
            # TODO: This doesn't work
            [_, feats] = zip(*examples)
            models['mean'] = np.append(models['mean'],
                                       np.array(map(np.mean, feats),)
            models['sigma'] = np.cov(feats, rowvar=0)
        else:
            models['mean'] = np.array(map(np.mean, feats))
            models['sigma'] = np.cov(feats, rowvar=0)

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
