// Coordinates are millimetres relative to the hopper flange's lower face.
// Socket values are editable assumptions, not SG90 manufacturer specifications.
export function fitState({ extension=2, mouthGap=.6, socketDepth=2.8, packing=0 }={}) {
  const bossFace=-1.3, shaftTip=-4.5;
  const contact=shaftTip-extension, mouth=bossFace-mouthGap, bottom=mouth-socketDepth;
  const gateBottom=contact-1.4-packing, gap=-(gateBottom+7.4);
  const overlap=Math.max(0,Math.min(bossFace,mouth)-Math.max(shaftTip,bottom));
  const tipClearance=shaftTip-bottom;
  return {bossFace,shaftTip,contact,mouth,bottom,gateBottom,gap,overlap,tipClearance,
    hubBottom:Math.min(contact,bottom-.6),
    gateInterference:gap<-.00001, gapInRange:gap>=.39999&&gap<=.80001,
    shaftBottomsOut:tipClearance<-.00001, bossInterference:mouthGap<-.00001,
    screeningEngagementPass:overlap>=2};
}

// Intersection area of the two actual radius-7 outlet circles. This is a
// geometric aperture only; it is not a powder mass-flow or dose calibration.
export function outletOverlapArea(angleDegrees,radius=7,shaftOffset=35){
 const d=2*shaftOffset*Math.abs(Math.sin(angleDegrees*Math.PI/360));
 if(d>=2*radius)return 0;
 if(d<1e-10)return Math.PI*radius*radius;
 return 2*radius*radius*Math.acos(d/(2*radius))-.5*d*Math.sqrt(4*radius*radius-d*d);
}
