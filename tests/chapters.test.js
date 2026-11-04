import test from 'node:test';
import assert from 'node:assert/strict';
import { chapters, chapterAt, startTime, totalDuration } from '../src/chapters.js';
test('timeline boundaries select exactly one chapter',()=>{for(const c of chapters){assert.equal(chapterAt(startTime(c.id)).chapter.id,c.id);assert.equal(chapterAt(startTime(c.id)+c.duration-.001).chapter.id,c.id);}assert.equal(chapterAt(totalDuration).chapter.id,chapters.length-1);});
test('instructions retain hardware constraints',()=>{const text=JSON.stringify(chapters);for(const term of ['GPIO19','GPIO18','400-point','USB-C','both retaining','3.3V','5V'])assert.ok(text.toLowerCase().includes(term.toLowerCase()));assert.equal(chapters.length,17);});
