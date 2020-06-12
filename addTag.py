#// Mohamad Janati
#// AmirHassan Asvadi ;)
#// Copyright (c) 2020 Mohamad Janati (freaking stupid, right? :|)

from aqt import mw
from aqt.reviewer import Reviewer
from anki.hooks import wrap
from aqt.utils import getTag, tooltip
from anki.utils import intTime, ids2str

config = mw.addonManager.getConfig(__name__)
tag1 = config['Tag 1']
tag2 = config['Tag 2']
deckName = config['Deck Name']

def myfunc(ids):
    mod = intTime()
    did = mw.col.decks.id(deckName)
    usn = mw.col.sched.col.usn()
    scids = ids2str(ids)
    mw.col.sched.remFromDyn(ids)
    mw.col.sched.col.db.execute("""
    update cards set usn=?, mod=?, did=? where id in """ + scids, usn, mod, did)

def _shortcutKeys_wrap(self, _old):
    def quick_tag():
        note = mw.reviewer.card.note()
        note.addTag(tag1)
        tooltip('Added tag "%s"' % tag1)
        note.flush()
    def quick_tag_n_move():
        note = mw.reviewer.card.note()
        note.addTag(tag2)
        note.flush()
        self.mw.checkpoint(_("Change Deck"))
        myfunc([self.card.id])
        tooltip('Added tag "%s" and moved' % tag2)
        self.mw.reset()
    def quick_move():
        note = mw.reviewer.card.note()
        self.mw.checkpoint(_("Change Deck"))
        myfunc([self.card.id])
        tooltip('Card moved to "%s"' % deckName)
        self.mw.reset()
    def custom_tag():
        note = mw.reviewer.card.note()
        (tagString, r) = getTag(mw, mw.col, 'Choose a tag:')
        note.addTag(tagString)
        tooltip('Added tag "%s"' % tagString)
        note.flush()
    old_list = _old(self)
    old_list.extend([
    ("Ctrl+S", lambda: quick_tag()),  #//Customize shortcuts here
    ("Ctrl+d", lambda: quick_tag_n_move()),  #//and here
    ("Ctrl+f", lambda: quick_move()),  #//and here
    ("Ctrl+g", lambda: custom_tag())  #//and here
    ])
    return old_list

Reviewer._shortcutKeys = wrap(Reviewer._shortcutKeys, _shortcutKeys_wrap, 'around')
