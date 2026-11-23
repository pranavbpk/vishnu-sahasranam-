"""Make audio/segends.json: for each verse, where line 1 (and the two half-line parts) should STOP
so the last syllable is never clipped. We stop just before the next part starts (next sound - 0.04 s),
never earlier than the original cut. Run after changing cuts.json / pada.json or re-recording a verse."""
import json,subprocess,numpy as np
cuts=json.load(open('audio/cuts.json'));pada=json.load(open('audio/pada.json'))
def env(n):
    raw=subprocess.run(['ffmpeg','-v','quiet','-i',f'audio/v{int(n):03d}.m4a','-ac','1','-ar','8000','-f','s16le','-'],capture_output=True).stdout
    a=np.frombuffer(raw,dtype=np.int16).astype(float);k=len(a)//80
    db=20*np.log10(np.sqrt((a[:k*80].reshape(k,80)**2).mean(1))+1);return db,db.max()
def endAt(db,thr,t):
    i=int(round(t*100))
    if i>=len(db):return t
    hi=i
    while hi<len(db)-1 and db[hi]<thr: hi+=1   # next sound after the cut
    lo=i
    while lo>0 and db[lo]<thr: lo-=1            # end of the sound before the cut
    if db[i]>=thr:                                # cut sits on sound: run to the end of that sound
        j=i
        while j<len(db)-1 and db[j]>=thr: j+=1
        return round(max(t,j/100+0.06),2)
    return round(max(t,min(hi/100-0.04,t+0.35)),2)
out={};st=[]
for n in cuts:
    db,pk=env(n);thr=np.percentile(db,95)-30
    c=endAt(db,thr,cuts[n]);p=pada.get(n,{}).get('t',[])
    out[n]={'c':c,'p':[endAt(db,thr,x) for x in p]}
    st.append(c-cuts[n])
json.dump(out,open('audio/segends.json','w'),separators=(',',':'))
print('verses',len(out),'line-1 end moved later by: median %.2f s, max %.2f s'%(np.median(st),max(st)))
