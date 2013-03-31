from django.http import HttpResponse
from django.shortcuts import render, redirect
from scrape import get_bricklist_peeron as get_bricklist
from models import LegoBricks, LegoSets
import smtplib
from email.mime.text import MIMEText

def index(request):
    return render(request, 'index.html', {})

def diff(request):
    setno = request.GET['setno']

    # Try loading from database.
    setdata = LegoSets.objects.filter(setno=setno)

    if not len(setdata):
        # Fallback to loading off of brickset directly.
        rawbricks = get_bricklist(setno)
        if not rawbricks:
            return render(request, 'noparts.html', {'setno': setno})
        for count, b in rawbricks:
            brick = LegoBricks(uid = b.uid,
                               partno = b.partno,
                               color = b.color,
                               description = b.description,
                               image_url = b.image_url)
            brick.save()
            setitem = LegoSets(setno=setno, count=count, brick=brick)
            setitem.save()
        setdata = LegoSets.objects.filter(setno=setno)

    return render(request, 'diff.html', {'bricks': setdata, 'setno': setno})

def result(request):
    setno = request.POST['setno']

    # Query all items in the set.
    setdata = LegoSets.objects.filter(setno=setno)

    # Remove all of the items that we returned as having.
    setcounts = {setitem.brick.uid: setitem.count for setitem in setdata}
    for k, v in request.POST.iteritems():
        try:
            v = int(v)
        except ValueError:
            continue

        if k in setcounts:
            setcounts[k] -= v
    setcounts = {uid: {'count': count} for uid, count in setcounts.items() if count > 0}

    # Add data to the counts.
    for setitem in setdata:
        uid = setitem.brick.uid
        if uid in setcounts:
            setcounts[uid]['description'] = setitem.brick.description
            setcounts[uid]['color'] = setitem.brick.color
            setcounts[uid]['partno'] = setitem.brick.partno
            setcounts[uid]['image_url'] = setitem.brick.image_url

    return render(request, "result.html", {'setno': setno, 'counts': setcounts})

