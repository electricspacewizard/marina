DROP TABLE IF EXISTS public.boats;

CREATE TABLE public.lifts(
    boat_id character varying(200),
    direction character varying(200),
    lift_time timestamp(200),
    paid boolean
);

CREATE TABLE public.boats(
    id serial primary key,
    bname character varying(200),
    btype character varying(200),
    loa decimal,
    beam decimal,
    draft decimal,
    keel_type character varying(200),
    dead_weight decimal,
    shaft_type character varying(200),

    spreader character varying(200),
    strop_type character varying(200),
    links_fwd decimal,
    links_aft decimal,
    cradle_type character varying(200),
    fwd_strop_pos character varying(200),
    aft_strop_post character varying(200),
    mast character varying(200)
);

ALTER TABLE public.boats OWNER TO marina;

INSERT INTO public.boats(
    bname, btype, loa, beam, draft, keel_type, dead_weight, shaft_type,
    spreader, strop_type, links_fwd, links_aft, cradle_type, fwd_strop_pos, aft_strop_post, mast)
    VALUES ('Landfall', 'Nauticat 33', 10.06, 3.23, 1.55, 'Longish', 10.6, 'Exposed',
      'Mid', 'Long', 10, 14, '10TUniversal', 'By Stanchion', '6 ahead of stanchion (Shaft starts at stanchion)', 'Up');