DROP TABLE IF EXISTS public.boats;

CREATE TABLE public.boats(
    id serial primary key,
    bname character varying(200),
    btype character varying(200),
    loa decimal,
    beam decimal,
    draft decimal,
    keel_type character varying(200),
    dead_weight character varying(200),
    shaft_type character varying(200),

    spreader character varying(200),
    strop_type character varying(200),
    links_fwd decimal,
    links_aft decimal,
    cradle_type character varying(200),
    fwd_strop_pos character varying(200),
    aft_strop_post character varying(200),
    mast character varying(200),
    notes text
);

CREATE TABLE public.lifts(
  lift_date timestamp default NULL,
  direction character varying(10),
  boat_id integer,
  paid boolean
);

ALTER TABLE public.boats OWNER TO marina;

INSERT INTO public.boats(
    bname, btype, loa, beam, draft, keel_type, dead_weight, shaft_type,
    spreader, strop_type, links_fwd, links_aft, cradle_type, fwd_strop_pos, aft_strop_post, mast)
    VALUES ('Landfall', 'Nauticat 33', 10.06, 3.23, 1.55, 'Longish', 10.6, 'Exposed',
      'Mid', 'Long', 10, 14, '10TUniversal', 'By Stanchion', '6" ahead of stanchion (Shaft starts at stanchion)', 'Up');

INSERT INTO public.boats(
    bname, btype, loa, beam, draft, keel_type, dead_weight, shaft_type,
    spreader, strop_type, links_fwd, links_aft, cradle_type, fwd_strop_pos, aft_strop_post, mast)
    VALUES ('Goldeneye', 'Najad 380', 11.58, 3.65, 1.59, 'Fin', '12T inc Spreader', 'Exposed',
      'Mid', '9m', 20, 28, '12T Uni', 'Just forward of mast', '1" aft of gate', 'Up');


INSERT INTO public.lifts(lift_date, direction, boat_id, paid)
VALUES(TIMESTAMP '30-03-2019 15:30:00', 'in', 1, true)
