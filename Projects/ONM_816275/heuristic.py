### This heuristic organizes ONM (818275) data on Flywheel
###
### Ellyn Butler
### September 6, 2019

import os

# create a key
def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

def ReplaceSubject(subj_label):
    return subj_label.lstrip('0')

t1w_moco = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-moco_T1w')


def gather_session_indeces():

    # use flywheel to gather a dict of all session session_labels
    # with their corresponding index by time, within the subject

    # query subjects
    import flywheel

    fw = flywheel.Client()

    cs = fw.projects.find_first('label="{}"'.format("ONM_816275"))
    cs_sessions = cs.sessions()
    cs_subjects = [fw.get(x.parents.subject) for x in cs_sessions]
    #cs_subject_labs = [int(x.label) for x in cs_subjects]

    # initialise dict
    sess_dict = {}

    for x in range(len(cs_subjects)):
        # get a list of their sessions
        sess_list = cs_subjects[x].sessions()

        if sess_list:
            # sort that list by timestamp
            sess_list = sorted(sess_list, key=lambda x: x.label) #Not sure this works

            # loop through the sessions and assign the session label an index
            for i, y in enumerate(sess_list):
                sess_dict[y.label] = "ONM" + str(i + 1) #!!!!!!!!

    return sess_dict

sessions = gather_session_indeces()

def ReplaceSession(ses_label):
    return str(sessions[ses_label])



def infotodict(seqinfo):
    # create the heuristic
    info = {t1w_moco: []}

    for s in seqinfo:
        protocol = s.protocol_name.lower()
        # t1
        if "mprage" in protocol and 'nav' not in protocol and 'moco' in protocol and s.TR == 1.85 and s.dim1 == 256 and "DERIVED" not in s.image_type:
            info[t1w_moco].append(s.series_id)
    return info





#import flywheel

#client = flywheel.Client()
#conte = client.projects.find_first('label=CONTE_815814')

#for subject in conte.subjects():
#    for session in subject.sessions():
#        for acq in session.acquisitions():
#            if acq['classification'] == {}:
