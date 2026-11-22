// 105
  105: {
    bounds: [boboHome, POI['jamesBarnesHome'].coord, POI['fiveForks'].coord],
    zoom: { desktop: 11, mobile: 10 },
    action() {
      setClock('7:44 AM', 'Apr 13, 2011');
      const a = drawPOI('boboHome', { pos: 'above', gap: 20}); 
      const b = drawPOI('jamesBarnesHome', { pos: 'above', gap: 20 }); 
      const c = drawPOI('fiveForks', { pos: 'above', gap: 20 }); 
      makeDot(boboHome, COLORS.holly, 9, true);
      makeDot(jamesBarnesHome, COLORS.holly, 9, true);
      makeDot(fiveForks, COLORS.holly, 9, true);
      drawLine(boboHome, fiveForks, '~4 min', [0, 0.0001]);
    }
},




