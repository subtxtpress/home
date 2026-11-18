// 61
  61: {
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
// 62
  62: {
    bounds: [boboHome, POI['jamesBarnesHome'].coord, POI['fiveForks'].coord],
    zoom: { desktop: 11, mobile: 10 },
    action() {
      setClock('7:45 AM', 'Apr 13, 2011');
      const a = drawPOI('boboHome', { pos: 'above', gap: 20}); 
      const b = drawPOI('jamesBarnesHome', { pos: 'above', gap: 20 }); 
      const c = drawPOI('fiveForks', { pos: 'above', gap: 20 }); 
      makeDot(boboHome, COLORS.holly, 9, true);
      makeDot(jamesBarnesHome, COLORS.holly, 9, true);
      makeDot(fiveForks, COLORS.holly, 9, true);
      drawLine(boboHome, fiveForks, '~4 min', [0, 0.0001]);
    }
},
// 63
  63: {
    bounds: [boboHome, POI['jamesBarnesHome'].coord, POI['scottsHillMiddleSchool'].coord],
    zoom: { desktop: 19, mobile: 18 },
    action() {
      setClock('7:47 AM', 'Apr 13, 2011');
      const a = drawPOI('boboHome', { pos: 'above', gap: 20}); 
      const b = drawPOI('jamesBarnesHome', { pos: 'below', gap: 20 }); 
      const c = drawPOI('scottsHillMiddleSchool', { pos: 'above', gap: 20 }); 
      makeDot(boboHome, COLORS.holly, 9, true);
      makeDot(jamesBarnesHome, COLORS.holly, 9, true);
      makeDot(scottsHillMiddleSchool, COLORS.holly, 9, true);
      drawLine(boboHome, scottsHillMiddleSchool, '~25 min', [0, 0.0001]);
    }
},
// 64
  64: {
    bounds: [boboHome, POI['drewScottWork'].coord, POI['foodGiant'].coord],
    zoom: { desktop: 11, mobile: 10 },
    action() {
      setClock('7:50 AM', 'Apr 13, 2011');
      const a = drawPOI('boboHome', { pos: 'above', gap: 20}); 
      const b = drawPOI('drewScottWork', { pos: 'above', gap: 20 }); 
      const c = drawPOI('foodGiant', { pos: 'above', gap: 20 }); 
      makeDot(boboHome, COLORS.holly, 9, true);
      makeDot(drewScottWork, COLORS.holly, 9, true);
      makeDot(foodGiant, COLORS.holly, 9, true);
      drawLine(boboHome, drewScottWork, '~11 min', [0, 0.0003]);
    }
},
// 65
  65: {
    bounds: [boboHome, POI['dispatch_911'].coord],
    zoom: { desktop: 11, mobile: 10 },
    action() {
      setClock('7:51 AM', 'Apr 13, 2011');
      const a = drawPOI('boboHome', { pos: 'above', gap: 20}); 
      const b = drawPOI('dispatch_911', { pos: 'below', gap: 20 }); 
      makeDot(boboHome, COLORS.holly, 9, true);
      makeDot(dispatch_911, COLORS.holly, 9, true);
      drawLine(boboHome, dispatch_911, '~27 min', [0, 0.0002]);
    }
},





};