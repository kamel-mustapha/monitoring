import {
  trigger,
  state,
  transition,
  style,
  animate,
} from '@angular/animations';

export const animations = [
  trigger('fadeInOut', [
    state('void', style({ opacity: 0 })),
    transition('void <=> *', [animate(100)]),
  ]),
  trigger('slideInOut', [
    transition('void <=> *', [
      style({ transform: 'translateY(-20%)' }),
      animate(100),
    ]),
  ]),
  trigger('slideRight', [
    transition('void => *', [
      style({ transform: 'translateX(10%)' }),
      animate(100),
    ]),
  ]),
  trigger('slideTop', [
    transition('void => *', [style({ top: '-400px' }), animate(100)]),
  ]),
  trigger('scaleY', [
    transition('void <=> *', [style({ transform: 'scaleY(0)' }), animate(100)]),
  ]),
  trigger('slideTopShort', [
    transition('void => *', [
      style({ top: '-50px', opacity: 0, transform: 'scale(0.1)' }),
      animate(100),
    ]),
  ]),
];
