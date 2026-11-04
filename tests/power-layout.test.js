import test from 'node:test';
import assert from 'node:assert/strict';
import { CatmullRomCurve3, Vector3 } from 'three';
import { powerLayout as layout } from '../src/power-layout.js';

test('power wires leave the screw-terminal end, away from the USB plug',()=>{
  for(const route of layout.routes){
    assert.equal(route.points[0][0],layout.terminalX);
    assert.ok(route.points[1][0]>route.points[0][0]);
    assert.ok(route.points[0][0]>layout.brickCenter[0]+layout.brickSize[0]/2);
  }
  assert.equal(layout.routes.length,2);
});

test('curved power leads clear the entire brick rather than crossing its top or body',()=>{
  const minimum=layout.brickCenter.map((v,i)=>v-layout.brickSize[i]/2);
  const maximum=layout.brickCenter.map((v,i)=>v+layout.brickSize[i]/2);
  for(const route of layout.routes){
    const curve=new CatmullRomCurve3(route.points.map(p=>new Vector3(...p)));
    for(const point of curve.getPoints(1200)){
      const distance=Math.sqrt(point.toArray().reduce((sum,v,i)=>sum+Math.max(minimum[i]-v,0,v-maximum[i])**2,0));
      assert.ok(distance>.65,`Wire intersects the brick near ${point.toArray()}`);
    }
  }
});
