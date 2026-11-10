import test from 'node:test';
import assert from 'node:assert/strict';
import {fitState,outletOverlapArea} from '../src/fit-math.js';
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-8,`${a} != ${b}`);
test('nominal horn seats without bottoming and gate clearance is 0.5 mm',()=>{
 const s=fitState();near(s.gap,.5);near(s.overlap,2.6);near(s.tipClearance,.2);
 assert.ok(s.gapInRange&&!s.shaftBottomsOut);
});
test('packing moves the gate, not the seated horn or shaft engagement',()=>{
 const a=fitState(),b=fitState({packing:.8});near(b.gap-a.gap,.8);
 near(a.contact,b.contact);near(a.overlap,b.overlap);near(a.tipClearance,b.tipClearance);
});
test('bad socket and arm placement produce visible seating/gap failures',()=>{
 assert.ok(fitState({socketDepth:1.5}).shaftBottomsOut);
 assert.ok(fitState({mouthGap:-.1}).bossInterference);
 assert.ok(fitState({extension:0}).gateInterference);
 assert.ok(!fitState({mouthGap:1.5}).screeningEngagementPass);
});
test('outlet closes before 60 degrees and does not imply a mass-flow rate',()=>{
 near(outletOverlapArea(0),Math.PI*49);near(outletOverlapArea(60),0);
 assert.ok(outletOverlapArea(20)>0&&outletOverlapArea(20)<outletOverlapArea(10));
 near(outletOverlapArea(24),0);near(outletOverlapArea(-10),outletOverlapArea(10));
});
