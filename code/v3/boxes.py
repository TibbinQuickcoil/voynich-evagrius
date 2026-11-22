import json,re
B='/home/claude/zl/vu/data/voynich-units/morphometry_voynichese/voynichese_boxes/'
def load_boxes(p):
    t=open(B+p+'.js').read(); t=t[t.index('['):]
    voc,bx=json.loads(t)
    return [dict(w=voc[i][0],x=x,y=y,w_=w,h=h) for i,x,y,w,h in bx]
if __name__=='__main__':
    b=load_boxes('f106r'); xs=[q['x'] for q in b]; ys=[q['y'] for q in b]
    print(len(b),"tokens; x",min(xs),max(x['x']+x['w_'] for x in b),"y",min(ys),max(y['y']+y['h'] for y in b))
    print([ (q['w'],q['x'],q['y'],q['w_'],q['h']) for q in b[:8]])
