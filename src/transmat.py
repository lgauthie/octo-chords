import sys
import cPickle as pickle
import itertools

import numpy as np
import numpy.matlib as ml
import numpy.linalg as linalg
import matplotlib.pyplot as plt

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
    feats, _ = load_feats_labels(file_list)
    hmm.means_ = np.transpose(models['mean'])
    hmm.covars_ = models['sigma']
    features, labels = load_feats_labels(['audio.arff'])
    _, seq = hmm.decode(np.transpose(features))
    #print filter(lambda(x,y): x==y, zip(labels, map(int2label, seq)))
    print len(filter(lambda(x,y): x==y, zip(labels, map(int2label, seq))))
    pickle.dump(hmm, open(outname, "wb"))
    plt.imshow(transitions)
    plt.show()

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
            covars = np.cov(np.transpose(feats))
            if (not np.allclose(covars, covars.T)
                or np.any(linalg.eigvalsh(covars) <= 0)):
                print 'Invalid Covars, using globalcov'
                models['sigma'] = np.append(models['sigma'], globalcov)
            else:
                models['sigma'] = np.append(models['sigma'],
                                            np.cov(np.transpose(feats)))

        else:
            models['mean'] = np.append(models['mean'], globalmean)
            models['sigma'] = np.append(models['sigma'], globalcov)
    models['mean'] = models['mean'].reshape(12,models['mean'].size/12)
    models['sigma'] = models['sigma'].reshape(models['sigma'].size/(12*12),12,12)

    n = len(states)
    transitions = np.zeros(shape=(n,n))
    trans = zip(labels[0:-1], labels[1:])
    for (i, ikey) in enumerate(states):
        for (j, jkey) in enumerate(states):
            # Add one so there is no zero probabilities
            transitions[i,j] = 0.01 + sum([1 for (f, s) in trans
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
    quals = ['maj', 'min']#, 'aug', 'dim', 'sus2', 'sus4']
    labels = [note + ':' + qual for note in notes for qual in quals]
    labels.extend(['N'])
    return labels

_labels = get_labels()
def int2label(i):
    return _labels[i]

def label_filt(label):
    sp = label.split(':')
    if sp[0] in ['N', 'X']:
        return 'N'
    if sp[1] in ['dim']:
        return sp[0] + ':min'
    elif sp[1] in ['aug', 'sus2', 'sus4']:
        return sp[0] + ':maj'
    else:
        return label

def load_feats_labels(file_list):
    """ Read all chord labels from a list of files """
    features = []
    labels = []
    for path in file_list:
        with open(path, 'r') as f:
            contents = np.array(
                [l[0:-1].split(',') for l in f if not l[0] in ['%', '@', '\n'] and l[-1] != 'X']
            )
            labels.append([label_filt(label) for label in contents[:,-1]])
            features.append([map(float, feat) for feat in contents[:,0:-1]])
    features = list(itertools.chain(*features))
    features = np.array(features)
    features.shape = (12,features.size/12)
    labels = list(itertools.chain(*labels))
    labels = np.array(labels)
    labels.shape = (labels.size,)
    return (features, labels)

if __name__=="__main__":
    main()
