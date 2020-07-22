$(document).ready(function () {

    //clear all markers and polyline on the map
    stopsLayer.clearLayers();
    journeyLayer.clearLayers();

    showSearchJourneyDiv();
    initAutoComplete();
});


// var data = {
//     "geocoded_waypoints" : [
//        {
//           "geocoder_status" : "OK",
//           "place_id" : "ChIJ1ar75WUJZ0gR23_MTNhRDD4",
//           "types" : [
//              "establishment",
//              "movie_theater",
//              "point_of_interest",
//              "shopping_mall"
//           ]
//        },
//        {
//           "geocoder_status" : "OK",
//           "place_id" : "ChIJf8BPrFIMZ0gRQyNuwyqmRVY",
//           "types" : [ "neighborhood", "political" ]
//        }
//     ],
//     "routes" : [
//        {
//           "bounds" : {
//              "northeast" : {
//                 "lat" : 53.3607995,
//                 "lng" : -6.208698099999999
//              },
//              "southwest" : {
//                 "lat" : 53.2865507,
//                 "lng" : -6.3033644
//              }
//           },
//           "copyrights" : "Map data ©2020",
//           "legs" : [
//              {
//                 "arrival_time" : {
//                    "text" : "10:55pm",
//                    "time_zone" : "Europe/Dublin",
//                    "value" : 1595368511
//                 },
//                 "departure_time" : {
//                    "text" : "9:55pm",
//                    "time_zone" : "Europe/Dublin",
//                    "value" : 1595364922
//                 },
//                 "distance" : {
//                    "text" : "15.5 km",
//                    "value" : 15514
//                 },
//                 "duration" : {
//                    "text" : "1 hour 0 mins",
//                    "value" : 3589
//                 },
//                 "end_address" : "Saint James' (part of Phoenix Park), Dublin, Ireland",
//                 "end_location" : {
//                    "lat" : 53.3509348,
//                    "lng" : -6.3033644
//                 },
//                 "start_address" : "16 Sandyford Rd, Dundrum, Dublin, Ireland",
//                 "start_location" : {
//                    "lat" : 53.2865507,
//                    "lng" : -6.240381999999999
//                 },
//                 "steps" : [
//                    {
//                       "distance" : {
//                          "text" : "0.1 km",
//                          "value" : 135
//                       },
//                       "duration" : {
//                          "text" : "2 mins",
//                          "value" : 98
//                       },
//                       "end_location" : {
//                          "lat" : 53.28721789999999,
//                          "lng" : -6.2400552
//                       },
//                       "html_instructions" : "Walk to Dundrum Centre",
//                       "polyline" : {
//                          "points" : "}ofdIjyae@GU@E@I?G?MGUOc@]iAQZGJKPMXQ`@EH"
//                       },
//                       "start_location" : {
//                          "lat" : 53.2865507,
//                          "lng" : -6.240381999999999
//                       },
//                       "steps" : [
//                          {
//                             "distance" : {
//                                "text" : "9 m",
//                                "value" : 9
//                             },
//                             "duration" : {
//                                "text" : "1 min",
//                                "value" : 12
//                             },
//                             "end_location" : {
//                                "lat" : 53.2865907,
//                                "lng" : -6.2402657
//                             },
//                             "html_instructions" : "Head \u003cb\u003enortheast\u003c/b\u003e\u003cdiv style=\"font-size:0.9em\"\u003eTake the stairs\u003c/div\u003e",
//                             "polyline" : {
//                                "points" : "}ofdIjyae@GU"
//                             },
//                             "start_location" : {
//                                "lat" : 53.2865507,
//                                "lng" : -6.240381999999999
//                             },
//                             "travel_mode" : "WALKING"
//                          },
//                          {
//                             "distance" : {
//                                "text" : "66 m",
//                                "value" : 66
//                             },
//                             "duration" : {
//                                "text" : "1 min",
//                                "value" : 43
//                             },
//                             "end_location" : {
//                                "lat" : 53.2868383,
//                                "lng" : -6.2394199
//                             },
//                             "html_instructions" : "Turn \u003cb\u003eright\u003c/b\u003e toward \u003cb\u003eSandyford Rd\u003c/b\u003e",
//                             "maneuver" : "turn-right",
//                             "polyline" : {
//                                "points" : "epfdItxae@@E@I?G?MGUOc@]iA"
//                             },
//                             "start_location" : {
//                                "lat" : 53.2865907,
//                                "lng" : -6.2402657
//                             },
//                             "travel_mode" : "WALKING"
//                          },
//                          {
//                             "distance" : {
//                                "text" : "60 m",
//                                "value" : 60
//                             },
//                             "duration" : {
//                                "text" : "1 min",
//                                "value" : 43
//                             },
//                             "end_location" : {
//                                "lat" : 53.28721789999999,
//                                "lng" : -6.2400552
//                             },
//                             "html_instructions" : "Turn \u003cb\u003eleft\u003c/b\u003e onto \u003cb\u003eSandyford Rd\u003c/b\u003e\u003cdiv style=\"font-size:0.9em\"\u003eDestination will be on the left\u003c/div\u003e",
//                             "maneuver" : "turn-left",
//                             "polyline" : {
//                                "points" : "wqfdIjsae@QZGJKPMXQ`@EH"
//                             },
//                             "start_location" : {
//                                "lat" : 53.2868383,
//                                "lng" : -6.2394199
//                             },
//                             "travel_mode" : "WALKING"
//                          }
//                       ],
//                       "travel_mode" : "WALKING"
//                    },
//                    {
//                       "distance" : {
//                          "text" : "4.4 km",
//                          "value" : 4369
//                       },
//                       "duration" : {
//                          "text" : "11 mins",
//                          "value" : 660
//                       },
//                       "end_location" : {
//                          "lat" : 53.305526,
//                          "lng" : -6.2116124
//                       },
//                       "html_instructions" : "Bus towards Citywest - UCD",
//                       "polyline" : {
//                          "points" : "{sfdItwae@GIINILMTY`@U\\GLGNYp@i@zACFMXCHCHCHCH?BCFAFADCTG^CFEPEPGJEJGLU^U\\GHKL{@r@g@`@SNQPMJGHSVABo@dAYh@KP[d@]^WVw@r@]TSJKDKDIBI@MBc@D?@kAHSHmBCS|B_Bs@`BaHjC}K?AGEHYJ_@Rk@Tu@No@H]Li@F[Fa@D]Ba@@W@Y?_@?_@?]C]AWCWC[K{@Kw@E[CWEc@AY?IAK?K?I@U?k@Bi@D{@H_B?M@M@ULsCHqB@U?W@i@Ac@Ag@?UEi@Ei@E_@I_@COc@{Ag@_BMc@Qm@Mc@EOIYYgAQm@CISw@Qo@EMCMG[GSGk@?M?YNw@BY@U?S?ICi@OqC?EQwCEm@GgAGyAAMAOCYEo@IuAASC]O}ACUAIE[G[CKCKGYGU[cAYy@M[c@uAW{@]cAg@yAQg@GSEMGKEKMWYa@OWMMOQKIKISKMGKEUIMGKAOEMAWAQ@Q?SDOBQDc@Hw@NG@I@i@DQ?CAm@CMCk@UGCSIk@Ye@UYQm@_@g@YMGMIKKOMKMOWKQWm@?CM]CIMa@Qm@m@oBUq@Ok@[aAo@uBK]Mc@Y{@Ss@[cAMc@M_@Ma@K]Uw@ISWaAOc@]kAIUc@{AMa@c@uACM[aAOg@IWi@gBeAiDKYMa@K]g@cBa@p@u@lAwEpHk@|@[h@EHKNHP"
//                       },
//                       "start_location" : {
//                          "lat" : 53.2871836,
//                          "lng" : -6.240114
//                       },
//                       "transit_details" : {
//                          "arrival_stop" : {
//                             "location" : {
//                                "lat" : 53.305526,
//                                "lng" : -6.2116124
//                             },
//                             "name" : "Belfield, Seafiled Road"
//                          },
//                          "arrival_time" : {
//                             "text" : "10:08pm",
//                             "time_zone" : "Europe/Dublin",
//                             "value" : 1595365680
//                          },
//                          "departure_stop" : {
//                             "location" : {
//                                "lat" : 53.2871836,
//                                "lng" : -6.240114
//                             },
//                             "name" : "Dundrum Centre"
//                          },
//                          "departure_time" : {
//                             "text" : "9:57pm",
//                             "time_zone" : "Europe/Dublin",
//                             "value" : 1595365020
//                          },
//                          "headsign" : "Citywest - UCD",
//                          "line" : {
//                             "agencies" : [
//                                {
//                                   "name" : "Go-Ahead",
//                                   "url" : "http://www.transportforireland.ie/"
//                                }
//                             ],
//                             "short_name" : "175",
//                             "vehicle" : {
//                                "icon" : "//maps.gstatic.com/mapfiles/transit/iw2/6/bus2.png",
//                                "name" : "Bus",
//                                "type" : "BUS"
//                             }
//                          },
//                          "num_stops" : 11
//                       },
//                       "travel_mode" : "TRANSIT"
//                    },
//                    {
//                       "distance" : {
//                          "text" : "10.5 km",
//                          "value" : 10541
//                       },
//                       "duration" : {
//                          "text" : "31 mins",
//                          "value" : 1866
//                       },
//                       "end_location" : {
//                          "lat" : 53.3516967,
//                          "lng" : -6.297740500000001
//                       },
//                       "html_instructions" : "Bus towards Phoenix Pk",
//                       "polyline" : {
//                          "points" : "qfjdIpe|d@IQ_BfCmArBu@nAu@tAYf@?TADAFIRu@fBm@dB_DdJq@lB{@dCYj@KPa@x@INMRMTi@~@_@h@y@jA]\\YXYRKHSFM@GAKHi@`@IFk@^yA`ACB_An@{@j@s@h@[Z[V[`@A@c@p@q@jAUf@Sh@Of@Oj@WdAEPMp@[jA?B]hAMh@KZELo@fBSd@Uf@Uf@o@dAOXm@z@UZ[`@QXs@dA_@f@yAxByA`CmB`DGJy@pAILSZg@v@IJCF[h@]n@KRu@t@A@EDQHQXg@p@OPKNCB}AzBEFk@x@Yj@q@fAKLGJw@nA[h@GJ_@n@OXIPIROj@Q~BI^O^IRMXOTCFS^]p@Ub@{ArBINGFMRGHIJQT[^c@l@u@hAYb@aBbCGHGHm@z@W`@QTOTKRe@v@A@uApBIJUXy@fAc@j@m@x@s@fAi@t@c@v@CHITELITK\\GNW`A?@Mf@Wx@EPMd@Od@YdASr@Ur@KZMZA@Yx@AJ?BABIVK\\Of@Kb@AJG`@_@zDM~@Mn@On@K\\?B]~@U`@Ud@U\\Y^MNMLa@Xu@f@SHEBC@g@RGD]NA@aAn@KDSASNIFEBIFaAjAc@d@g@j@IHONONSRsBdCw@v@QPe@d@[\\i@f@g@h@m@p@FVGWOP[^EDkAnA_@h@KVEHEFIX[Si@_@KGy@i@YScAs@SQwB{A[Y[YGACAE?G?MDGBED?@EFCFGVEXAD]pBI`@GPUv@i@jDWnAYjAqAWu@Ow@Q?EkNkC[dC[xBIV[VWAg@Mu@@QBkAz@aBwAs@CsAFC?DH[@M?w@Ay@?y@C]CU?KBA@IBe@R[LMDMDSF}Br@IB]JKFI@mA`@SFkC|@{Af@aEtAa@Nk@PaA\\UHm@R]NOFH^~@pCPZR\\R\\]r@U`@g@|@a@t@uBbD_BnCu@tAEFKTCFOj@k@~Ba@vAi@jACFCDA@A@A?A?A@A?IFCBA@A@ADe@~BiAe@e@SKC_Bs@GAWEEAOCI?M?a@CW?E?MBQJKHSLk@f@y@r@KF[XA@i@d@aBxAo@j@]X{@DUAg@EYE_AMSASAIBC?A?G@C?E?E@E@A?A@A@C@C@CBCBCDGHG~@Av@C^EfAErAARC`AAHC~@Ad@AXAb@?j@?|B?r@?Z@vB?V@X?v@DNDNBHFRDRH\\Nz@l@hDh@rCv@`E^rBP~@Jj@?BVnA^tB\\lBZxADVd@hCVtANr@h@xCF^Hb@Hb@Hh@BPHv@@FPpAx@vGRbBJx@X`CRvABJBb@ZzDBRHr@Hr@DTBLDLDLDLHNP\\Xd@vBrDXd@h@z@PXdB`Dp@pAdAnBb@x@l@lAZl@Vd@@B~@dBZh@h@~@`AjBHL~@hB@@FHHHB@D@B?DADCHENQz@_AvAoAdAaA?AcDpD"
//                       },
//                       "start_location" : {
//                          "lat" : 53.305526,
//                          "lng" : -6.2116124
//                       },
//                       "transit_details" : {
//                          "arrival_stop" : {
//                             "location" : {
//                                "lat" : 53.3516967,
//                                "lng" : -6.297740500000001
//                             },
//                             "name" : "Arbour Hill, Phoenix Park Gate"
//                          },
//                          "arrival_time" : {
//                             "text" : "10:49pm",
//                             "time_zone" : "Europe/Dublin",
//                             "value" : 1595368156
//                          },
//                          "departure_stop" : {
//                             "location" : {
//                                "lat" : 53.305526,
//                                "lng" : -6.2116124
//                             },
//                             "name" : "Belfield, Seafiled Road"
//                          },
//                          "departure_time" : {
//                             "text" : "10:18pm",
//                             "time_zone" : "Europe/Dublin",
//                             "value" : 1595366290
//                          },
//                          "headsign" : "Phoenix Pk",
//                          "line" : {
//                             "agencies" : [
//                                {
//                                   "name" : "Dublin Bus",
//                                   "url" : "http://www.transportforireland.ie/"
//                                }
//                             ],
//                             "short_name" : "46a",
//                             "vehicle" : {
//                                "icon" : "//maps.gstatic.com/mapfiles/transit/iw2/6/bus2.png",
//                                "name" : "Bus",
//                                "type" : "BUS"
//                             }
//                          },
//                          "num_stops" : 32
//                       },
//                       "travel_mode" : "TRANSIT"
//                    },
//                    {
//                       "distance" : {
//                          "text" : "0.5 km",
//                          "value" : 469
//                       },
//                       "duration" : {
//                          "text" : "6 mins",
//                          "value" : 355
//                       },
//                       "end_location" : {
//                          "lat" : 53.3509348,
//                          "lng" : -6.3033644
//                       },
//                       "html_instructions" : "Walk to Saint James' (part of Phoenix Park), Dublin, Ireland",
//                       "polyline" : {
//                          "points" : "igsdIh_me@o@r@OPIDGDG?F~@?FV@E~@AXAJ?N?rA?p@@pA?~@@T?LBND\\BXLf@Rn@BL@HBJNh@Vv@Rl@INFJ\\h@^z@`@`AJN"
//                       },
//                       "start_location" : {
//                          "lat" : 53.3517306,
//                          "lng" : -6.297652299999999
//                       },
//                       "steps" : [
//                          {
//                             "distance" : {
//                                "text" : "58 m",
//                                "value" : 58
//                             },
//                             "duration" : {
//                                "text" : "1 min",
//                                "value" : 49
//                             },
//                             "end_location" : {
//                                "lat" : 53.35218039999999,
//                                "lng" : -6.2980646
//                             },
//                             "html_instructions" : "Head \u003cb\u003enorthwest\u003c/b\u003e on \u003cb\u003eInfirmary Rd\u003c/b\u003e/\u003cwbr/\u003e\u003cb\u003eR101\u003c/b\u003e toward \u003cb\u003eNorth Rd\u003c/b\u003e",
//                             "polyline" : {
//                                "points" : "igsdIh_me@o@r@OPIDGDG?"
//                             },
//                             "start_location" : {
//                                "lat" : 53.3517306,
//                                "lng" : -6.297652299999999
//                             },
//                             "travel_mode" : "WALKING"
//                          },
//                          {
//                             "distance" : {
//                                "text" : "24 m",
//                                "value" : 24
//                             },
//                             "duration" : {
//                                "text" : "1 min",
//                                "value" : 23
//                             },
//                             "end_location" : {
//                                "lat" : 53.3521392,
//                                "lng" : -6.2984241
//                             },
//                             "html_instructions" : "Turn \u003cb\u003eleft\u003c/b\u003e onto \u003cb\u003eNorth Rd\u003c/b\u003e",
//                             "maneuver" : "turn-left",
//                             "polyline" : {
//                                "points" : "cjsdIzame@F~@?F"
//                             },
//                             "start_location" : {
//                                "lat" : 53.35218039999999,
//                                "lng" : -6.2980646
//                             },
//                             "travel_mode" : "WALKING"
//                          },
//                          {
//                             "distance" : {
//                                "text" : "13 m",
//                                "value" : 13
//                             },
//                             "duration" : {
//                                "text" : "1 min",
//                                "value" : 11
//                             },
//                             "end_location" : {
//                                "lat" : 53.352023,
//                                "lng" : -6.298433800000001
//                             },
//                             "html_instructions" : "Turn \u003cb\u003eleft\u003c/b\u003e",
//                             "maneuver" : "turn-left",
//                             "polyline" : {
//                                "points" : "{isdIbdme@V@"
//                             },
//                             "start_location" : {
//                                "lat" : 53.3521392,
//                                "lng" : -6.2984241
//                             },
//                             "travel_mode" : "WALKING"
//                          },
//                          {
//                             "distance" : {
//                                "text" : "0.3 km",
//                                "value" : 275
//                             },
//                             "duration" : {
//                                "text" : "3 mins",
//                                "value" : 198
//                             },
//                             "end_location" : {
//                                "lat" : 53.351463,
//                                "lng" : -6.3022968
//                             },
//                             "html_instructions" : "Turn \u003cb\u003eright\u003c/b\u003e",
//                             "maneuver" : "turn-right",
//                             "polyline" : {
//                                "points" : "cisdIddme@E~@AXAJ?N?rA?p@@pA?~@@T?LBND\\BXLf@Rn@BL@HBJNh@Vv@Rl@"
//                             },
//                             "start_location" : {
//                                "lat" : 53.352023,
//                                "lng" : -6.298433800000001
//                             },
//                             "travel_mode" : "WALKING"
//                          },
//                          {
//                             "distance" : {
//                                "text" : "8 m",
//                                "value" : 8
//                             },
//                             "duration" : {
//                                "text" : "1 min",
//                                "value" : 6
//                             },
//                             "end_location" : {
//                                "lat" : 53.3515082,
//                                "lng" : -6.3023845
//                             },
//                             "html_instructions" : "Turn \u003cb\u003eright\u003c/b\u003e",
//                             "maneuver" : "turn-right",
//                             "polyline" : {
//                                "points" : "sesdIj|me@IN"
//                             },
//                             "start_location" : {
//                                "lat" : 53.351463,
//                                "lng" : -6.3022968
//                             },
//                             "travel_mode" : "WALKING"
//                          },
//                          {
//                             "distance" : {
//                                "text" : "91 m",
//                                "value" : 91
//                             },
//                             "duration" : {
//                                "text" : "1 min",
//                                "value" : 68
//                             },
//                             "end_location" : {
//                                "lat" : 53.3509348,
//                                "lng" : -6.3033644
//                             },
//                             "html_instructions" : "Turn \u003cb\u003eleft\u003c/b\u003e",
//                             "maneuver" : "turn-left",
//                             "polyline" : {
//                                "points" : "}esdIz|me@FJ\\h@^z@`@`AJN"
//                             },
//                             "start_location" : {
//                                "lat" : 53.3515082,
//                                "lng" : -6.3023845
//                             },
//                             "travel_mode" : "WALKING"
//                          }
//                       ],
//                       "travel_mode" : "WALKING"
//                    }
//                 ],
//                 "traffic_speed_entry" : [],
//                 "via_waypoint" : []
//              }
//           ],
//           "overview_polyline" : {
//              "points" : "}ofdIjyae@E[@QGc@m@mBs@rAWj@FHGIS\\g@v@]j@a@`A_AfCK`@Kj@WjAk@dA]f@gA`A{AnAmAjBe@z@y@dAoAjAq@`@k@Pq@H?@kAHSHmBCS|B_Bs@lF_UGG~@{Cn@sCL_ADy@@wBMiBa@gDIsA@wAn@}N@{BA}@KsAO_Ag@kBuAuEkB_HKi@O_A?g@RqA@i@Cs@g@}Ii@sJY{CUoAOo@u@}BgBqFgAcDMWg@y@]e@[[m@]{@Y]Gi@?e@Da@HmB\\{@Dq@EuAg@yCaBoAw@[[[i@i@yAkEsNmC{IaDqKyEqOY_Ag@cBa@p@mG~JgAfBQXHPIQmDzFkBdDYf@?TCL_AzBmEjMmBrFe@|@gArBiAhBy@jA]\\s@l@_@PU?u@j@sClB{BzAs@h@[Zw@x@e@r@gArBc@pAg@pBSbAgAbEuAvDkBnDqBrCsAlBsDzFyDlGiAfBy@xAKRu@t@GFQHQXw@bAKNsC`EkArBSX{BtDYj@Y~@Q~BI^Yr@u@vAs@tAeBbCg@p@m@t@yAvBkCzDgBhCiC~D}BxCaB`CmAlB]bAk@pBy@xCsArEu@rBMj@[dAMn@g@|E[nB[lA]bAk@fAo@|@[\\wA`A]NoAj@mAt@SASNOJkArAeBjBc@b@kD|D}B|BuAzAFVGWk@p@qAtAk@`AKPIX[Su@g@sA}@wAeAwDqCIAUDSRK^G^g@rC]hAaAzFYjAqAWmBa@?EkNkCw@~FIV[VWAg@Mu@@QBkAz@aBwAs@CsAFC?DHi@@qBAwAGa@BKD}Al@yDjAcQ~FqDlAm@VH^~@pCd@x@R\\]r@U`@iArBuErH{@|AO\\{@jDa@vAi@jAGLGBQLk@hCoBy@kBw@u@MqACSB]TeCpBiDzCmAdAqABuC[c@@WBKDOJKNIvBQnEKpDCfF@~E@pAJ^ZnA~CzPnDpRxClPdCbSt@hG^nERfBT~@z@`BlEnH`G|KbBdDfEzHrAbCLJH@JEXWz@_AvAoAdAcAcDpDEQ_AdAQJG?F~@?FV@GxAA`DBtDHl@P`A\\rAf@`BRl@INd@t@`A|BJN"
//           },
//           "summary" : "",
//           "warnings" : [
//              "Walking directions are in beta. Use caution – This route may be missing sidewalks or pedestrian paths."
//           ],
//           "waypoint_order" : []
//        }
//     ],
//     "status" : "OK"
//  }
 


function initAutoComplete(){

    //add restriction for autocomplete places API
    var options = {
        componentRestrictions: {country: "IE"}
    };

    var form_input = document.getElementById('form_input');
    var to_input = document.getElementById('to_input');

    function initAutocomplete(input){

        //use Google Place Autocomplete for input box
        //source: https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete
        var autocomplete = new google.maps.places.Autocomplete(input, options);

        // Set the data fields to return when the user selects a place.
        autocomplete.setFields(
            ['address_components', 'geometry', 'icon', 'name']);

        var infowindow = new google.maps.InfoWindow();
        var infowindowContent = document.getElementById('infowindow-content');
        infowindow.setContent(infowindowContent);
    

        autocomplete.addListener('place_changed', function() {
        infowindow.close();

        var place = autocomplete.getPlace();
        if (!place.geometry) {
            // User entered the name of a Place that was not suggested and
            // pressed the Enter key, or the Place Details request failed.
            window.alert("No details available for input: '" + place.name + "'");
            return;
        } 

        var address = '';
        if (place.address_components) {
            address = [
            (place.address_components[0] && place.address_components[0].short_name || ''),
            (place.address_components[1] && place.address_components[1].short_name || ''),
            (place.address_components[2] && place.address_components[2].short_name || '')
            ].join(' ');
        }

        infowindowContent.children['place-icon'].src = place.icon;
        infowindowContent.children['place-name'].textContent = place.name;
        infowindowContent.children['place-address'].textContent = address;
        });
    }

    initAutocomplete(form_input);
    initAutocomplete(to_input);
    
}


// submit button click event 
$('form').submit(function(e){
    // Stop form refreshing page on submit
    e.preventDefault();

    var origin = document.forms["journeyForm"]["f_from_stop"].value;
    var destination = document.forms["journeyForm"]["f_to_stop"].value;
    var dateTime = document.querySelector('input[type="datetime-local"]').value;

    // var origin = 'dundrum';
    // var destination = 'dun la';
    // var dateTime = '20';

    var dt = new Date(Date.parse(dateTime));
     //set departure time mins to 0,
    //if departure time given is 
    dt.setMinutes(0);
    var unix = dt.getTime()/1000;

    //get direction from api /api/direction
    $.getJSON(`http://127.0.0.1:8000/api/direction?origin=${origin}&destination=${destination}&departureUnix=${unix}`
    , function(data) {
        if (data.status == "OK"){
            try {
                var route = data.routes[0];
                var leg = route.legs[0];
                var arrive_time =  leg.arrival_time.text;
                var departure_time =  leg.departure_time.text;
                // var renderSteps = renderResultJourneySteps(leg.steps);
                var duration = leg.duration.text;
                // var transferCount = ((renderSteps.match(/bus_icon/g) || []).length).toString() ;
                
                displaySearchInfoOnHeader(origin, destination, dateTime);
                displayTripSummary(duration, '0', departure_time, arrive_time);
                displayJourneySteps(leg.steps);

                //drop destination marker
                dropMarkerOnMap(leg.end_location.lat, leg.end_location.lng, leg.end_address);
                //drop origin marker
                dropMarkerOnMap(leg.start_location.lat, leg.start_location.lng, leg.start_address);

                showResultJourneyDiv();

            } catch (error) {
                alert(error);
            }
        } else {
            alert("No journey planning result, please try input other locations.");
        }
        
    });
});

$('#edit_journey_input').click(function () {
    showSearchJourneyDiv();
    clearSearchResult();

});

//append value to key element
function displayElements(obj){
    $.each( obj, function( key, value ) {
        $(key).html(value);
    });
}


function displaySearchInfoOnHeader(origin, destination, dateTime){
    // dictionary to store all the elements which are going to display on frontend
    // key: the element id or class name
    // value: content to append to the element 
    var obj = {
        "#journey_result_from" : origin,
        "#journey_result_to" : destination,
        "#journey_result_datetime" : dateTime
    };
    displayElements(obj);
}

function displayTripSummary(duration, transferCount, departure_time, arrive_time){
    // dictionary to store all the elements which are going to display on frontend
    // key: the element id or class name
    // value: content to append to the element 
    // render duration and count of transfer 
    var duration_tranfer_count = renderContent({"Total duration:" : "<b>" + duration + "</b>" 
                                + "&nbsp;&nbsp;&nbsp;&nbsp;" 
                                + "<b>" + transferCount + "</b>" 
                                + "  transfers"});

    var obj = {
        "#journey_result_detail" : duration_tranfer_count,
        "#section-trip-summary" : departure_time + " &nbsp;&nbsp; <b style='font-size: 30px;'> &#8250; </b>  &nbsp;&nbsp;" + arrive_time,
                    
    };
    displayElements(obj);

}




function renderTransitStop(timeline, name, coordinates){
    content = '<div class="transit-stop row" > ';
    content += `<div class="transit-timeline col-2"><p>${timeline}</p></div>`
    content += '<div class="transit-stop-circle col-1">o</div>';
    content += `<div class="transit-stop-name col-9"><p>${name}</p></div>`;
    content += '</div>'

    return content;
}




function renderTransitDetail(step, index){

    content = '<div class="transit-stop row"> ';
    if (step.travel_mode == "TRANSIT"){
        content += `<div class="transit-timeline col-2"><img src="./static/img/bus_small.png" alt="bus_icon" class="journey_result_icon"></div>`
        content += '<div class="verticalLine col-1" style="border-left: 3px solid #ff0000;"></div>';

    } else {
        content += `<div class="transit-timeline col-2"><img src="./static/img/walking_small.png" alt="walk_icon" class="journey_result_icon"></div>`
        content += '<div class="transit-stop-circle col-1" style="border-left: 3px dotted #ff0000;">o</div>';
    }

    content +=  '<div class="transit-detail col-9">';
    content +=  `<div class="transit-mode row">${step.travel_mode}</div>`;
    content +=  `<div class="transit-duration row">${step.duration.text}&nbsp;&nbsp;&nbsp;&nbsp;${step.distance.text}</div>`;

    if (step.travel_mode == "TRANSIT"){
        content += renderStepCard(step, index);
        // content +=  `<div class="transit-num-stops row">${step.transit_details.num_stops}</div>`;
    }

    content += '</div></div>'

    return content;
}



function displayJourneySteps(steps){
    content = '';
    $.each( steps, function( index, step ) {
        // var isLastElement = index == data.length -1;
        // if (index == 0) {
        //     content += renderTransitStop(timeline, name, coordinates);
        
        // } else if (isLastElement) {

        // } else {

        // }
        

        if (step.travel_mode == "TRANSIT"){

            var transit_details = step.transit_details;
            content += renderTransitStop(transit_details.departure_time.text, 
                transit_details.departure_stop.name,
                transit_details.departure_stop.location);

            content += renderTransitDetail(step, index);

            content += renderTransitStop(transit_details.arrival_time.text, 
                transit_details.arrival_stop.name,
                transit_details.arrival_stop.location);



        } else if (step.travel_mode == "WALKING") {
            content += renderTransitDetail(step, index);
        }


        //get encoding journey polyline
        var encodingPolyline = step.polyline.points;
        //decode polyline to latlngs array
        var coordinates = decode(encodingPolyline);
        
        drawPolylineOnMap(step.travel_mode, coordinates);

        //drop destination marker
        dropMarkerOnMap(step.end_location.lat, step.end_location.lng, '');
    });

    displayElements({"#journey_result_steps" : content});
}



function renderStepCard(step, index){

    content = "";

    
    // Using the card component, show the steps of journey on card header
    // show detail of each step in card body 
    // resource: https://getbootstrap.com/docs/4.0/components/collapse/
    content += `
        <div class="card"> 
        <div class="card-header" id="heading${index}"><h5 class="mb-0">
        <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse${index}" aria-expanded="false" aria-controls="collapse${index}">`;
    
    content +=  `<div class="transit-num-stops row">${step.transit_details.num_stops} stops </div>`;

     
    // add journey steps detail in card body
    content += `
        </button></h5></div>
        <div id="collapse${index}" class="collapse" aria-labelledby="heading${index}" data-parent="#journey_result_steps">
        <div class="card-body">`;


    // if the travel_mode is TRANSIT, add bus icon and bus route number to content
    var stops = step.transit_details.stops;
        
   if (stops) {
        $.each(stops, function( index, value ) {
            content += "<p> " + value.plate_code + "  " + value.stop_name + "</p>";
        });

        //show number of stops
        content += "<p>Stops: <b>" + stops.length + "</b></p>";
    } else {
        content += "<p>" + step.html_instructions + "</p>";
    }
    content += '</div></div></div>';
    
    return content;

}



// // render result journey steps
// function renderResultJourneySteps(steps) {
//     //  TODO: handling when no bus journey, steps will become 0

//     content = '';
//     $.each( steps, function( index, step ) {

//         // Using the card component, show the steps of journey on card header
//         // show detail of each step in card body 
//         // resource: https://getbootstrap.com/docs/4.0/components/collapse/
//         content += `
//             <div class="card"> 
//             <div class="card-header" id="heading${index}"><h5 class="mb-0">
//             <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse${index}" aria-expanded="false" aria-controls="collapse${index}">`;
    
//         // if the travel_mode is TRANSIT, add bus icon and bus route number to content
//         if (step.travel_mode == "TRANSIT"){
//             var line = step.transit_details.line;
//             content +=  `<img src="./static/img/bus_small.png" alt="bus_icon" class="journey_result_icon"> &nbsp;`;
//             content += line.short_name;

//         // if the travel_mode is WALKING, add walk icon to content
//         } else if (step.travel_mode == "WALKING") {
//             content +=  `<img src="./static/img/walking_small.png" alt="walk_icon" class="journey_result_icon"> Walking`;
//         }

//         // add duration for the step to content
//         content += " (" + step.duration.text + ") ";

//         // add journey steps detail in card body
//         content += `
//             </button></h5></div>
//             <div id="collapse${index}" class="collapse" aria-labelledby="heading${index}" data-parent="#journey_result_steps">
//             <div class="card-body">`;
//         content += "<p>Distance: <b>" + step.distance.text + "</b></p>";
//         // if the travel_mode is TRANSIT, add bus icon and bus route number to content
//         if (step.travel_mode == "TRANSIT"){

//             var stops = step.transit_details.stops;
            
//             if (stops) {
//                 $.each(stops, function( index, value ) {
//                     content += "<p> " + value.plate_code + "  " + value.stop_name + "</p>";
//                 });

//                 //show number of stops
//                 content += "<p>Stops: <b>" + stops.length + "</b></p>";
//             }


//         // if the travel_mode is WALKING, add walk icon to content
//         } else if (step.travel_mode == "WALKING") {
//             content += "<p>" + step.html_instructions + "</p>";
//         }
//         content += '</div></div></div>';
      
//     });
//     return content
// }

function renderContent(obj){ 
    content = '<p>';
    $.each( obj, function( key, value ) {
        content += key;
        content += '  ';
        content += value;
        content += '<br>'
    });
    content += '</p>';
    return content
}


function dropMarkerOnMap(lat, lon, location){
 
    var marker = L.marker([lat, lon]) .bindPopup(`<b> ${location}</b>`);
    journeyLayer.addLayer(marker);
}


function drawPolylineOnMap(travel_mode, points){

    if (travel_mode == "TRANSIT"){
        var polyline = L.polyline(points, {color: 'red'});
    } else {
        var polyline = L.polyline(points, {color: 'red',  dashArray: '6, 6', dashOffset: '1'});
    }

    
    journeyLayer.addLayer(polyline);
    // zoom the map to the polyline
    map.fitBounds(polyline.getBounds());
}


function clearSearchResult(){
    var obj = {
        "#journey_result_from" : "",
        "#journey_result_to" : "",
        "#journey_result_datetime" : "",
        "#section-trip-summary" : "",
        "#journey_result_steps" : "",
        "#journey_result_detail" : ""
    };

    displayElements(obj);
    journeyLayer.clearLayers();
    stopsLayer.clearLayers();
}


function showSearchJourneyDiv(){
    $("#journey_result_div").fadeOut(10);
    $("#journey_search_div").fadeIn(10);
}

function showResultJourneyDiv(){
    $("#journey_search_div").fadeOut(10);
    $("#journey_result_div").fadeIn(10);
}


// decoding encode polyline which get from google direction API
// decode encode polyline to array which storing all points [lat,lng]
// code from: https://gist.github.com/ismaels/6636986
function decode(encoded){

    // array that holds the points

    var points=[ ]
    var index = 0, len = encoded.length;
    var lat = 0, lng = 0;
    while (index < len) {
        var b, shift = 0, result = 0;
        do {

    b = encoded.charAt(index++).charCodeAt(0) - 63;//finds ascii                                                                                    //and substract it by 63
              result |= (b & 0x1f) << shift;
              shift += 5;
             } while (b >= 0x20);
       var dlat = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
       lat += dlat;
      shift = 0;
      result = 0;
     do {
        b = encoded.charAt(index++).charCodeAt(0) - 63;
        result |= (b & 0x1f) << shift;
       shift += 5;
         } while (b >= 0x20);
     var dlng = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
     lng += dlng;
 
   points.push([(lat / 1E5), ( lng / 1E5)])  
 
  }
  return points
}