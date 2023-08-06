----------------------------------------------------------------------------
-- xplordb
-- 
-- Copyright (C) 2022  Oslandia / OpenLog
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU Affero General Public License as published
-- by the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU Affero General Public License for more details.
-- 
-- You should have received a copy of the GNU Affero General Public License
-- along with this program.  If not, see <https://www.gnu.org/licenses/>.
-- 
-- __authors__ = ["davidms"]
-- __contact__ = "geology@oslandia.com"
-- __date__ = "2022/02/02"
-- __license__ = "AGPLv3"
----------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION dh.dh_trace (character varying, character varying)
    RETURNS void
    LANGUAGE sql
    AS $function$
    --xplordb - Mineral Exploration Database template/ system for Postgres/PostGIS. The project incorporates perl import scripts; drillling, surface and QA/QC data and more.
    --Copyright (C) 2017  Light Catcher Pty Ltd
    --This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
    --This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
    --You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
    WITH RECURSIVE
    --select the collars
    collar AS (
        SELECT
            hole_id,
            x,
            y,
            z,
            max_depth,
            srid
        FROM
            dh.collar_view
        WHERE
            data_set = $1
            AND hole_id LIKE $2
),
--select the dh surveys
surv_body AS (
    SELECT
        hole_id,
        depth_m,
        dip,
        azimuth_grid
    FROM
        dh.surv
    WHERE
        hole_id IN (
            SELECT
                hole_id
            FROM
                collar)
),
--select the hole that have a dh survey at the end of hole
surv_at_eoh AS ((
        SELECT
            hole_id
        FROM
            collar
        WHERE
            ROW (hole_id,
                max_depth) IN (
                SELECT
                    hole_id,
                    max(depth_m)
                FROM
                    surv_body
                GROUP BY
                    hole_id))
),
--generate dh surveys at the eoh where there is no survey at the end of hole
surv_eoh AS (
    SELECT
        c.hole_id,
        c.max_depth,
        m.dip AS dip,
        m.azimuth_grid AS azimuth_grid
    FROM
        collar c,
        ( SELECT DISTINCT ON (hole_id)
                hole_id,
                max(dip) OVER max_surv AS dip,
                    max(azimuth_grid) OVER max_surv AS azimuth_grid
                    FROM
                        surv_body
WINDOW max_surv AS (PARTITION BY hole_id ORDER BY depth_m DESC)) m
WHERE (c.hole_id = m.hole_id)
AND c.hole_id NOT IN (
    SELECT
        hole_id
    FROM
        surv_at_eoh) --exclude holes that have a down hole survey at the end of hole
),
--select holes that have no dh survey at the collar
surv_no_coll AS (
    SELECT
        hole_id,
        dip,
        azimuth_grid
    FROM
        surv_body
    WHERE
        ROW (hole_id,
            depth_m) IN (
            SELECT
                hole_id,
                min(depth_m)
            FROM
                surv_body
            GROUP BY
                hole_id
            HAVING
                min(depth_m) != 0)
),
--merge the survey tables
surv_merge AS (
    SELECT
        hole_id,
        depth_m,
        dip,
        azimuth_grid
    FROM
        surv_body
    UNION ALL
    SELECT
        hole_id,
        max_depth,
        dip,
        azimuth_grid
    FROM
        surv_eoh
    UNION ALL
    SELECT
        hole_id,
        0,
        - 90,
        0
    FROM
        collar
    WHERE
        hole_id NOT IN (
            SELECT
                hole_id
            FROM
                surv_body) --holes that don't have a downhole survey are given a vertical dip at the "collar"
        UNION ALL
        SELECT
            hole_id,
            max_depth,
            - 90,
            0
        FROM
            collar
        WHERE
            hole_id NOT IN (
                SELECT
                    hole_id
                FROM
                    surv_body) --holes that don't have a downhole survey are given a vertical dip at the "end of hole"
            UNION ALL
            SELECT
                hole_id,
                0,
                dip,
                azimuth_grid
            FROM
                surv_no_coll
),
--
surv AS (
    SELECT
        hole_id,
        depth_m,
        lead_depth_m,
        dip,
        lead_dip,
        azimuth_grid,
        lead_azimuth_grid,
        CASE dog_leg
        WHEN 0 THEN
            1
        ELSE
            (2 / (dog_leg) * (tan(((dog_leg)) / 2)))
        END AS ratio_factor
    FROM (
        SELECT
            hole_id,
            depth_m,
            lead(depth_m) OVER (PARTITION BY hole_id ORDER BY hole_id,
                depth_m)::double precision AS lead_depth_m,
            d AS dip,
            lead(d) OVER (PARTITION BY hole_id ORDER BY hole_id,
                depth_m)::double precision AS lead_dip,
            azimuth_grid,
            lead(azimuth_grid) OVER (PARTITION BY hole_id ORDER BY hole_id,
                depth_m)::double precision AS lead_azimuth_grid
        FROM
            surv_merge s,
            LATERAL (
                SELECT
                    (90 - (dip * - 1))::double precision AS d) ld) sub_query,
            LATERAL (
                SELECT
                    dh.dog_leg (dip, lead_dip, azimuth_grid, lead_azimuth_grid) AS dog_leg) dl_sub_query
),
--the displacements at each survey point
results AS (
    --minimum curvature method
    SELECT
        hole_id,
        depth_m,
        --x
        (((lead_depth_m - depth_m) / 2) * (sin(radians(dip)) * (sin(radians(azimuth_grid))) + (sin(radians(lead_dip))) * (sin(radians(lead_azimuth_grid))))) * ratio_factor AS x,
        --y
        ((((lead(depth_m, 1) OVER w) - depth_m) / 2) * (sin(radians(dip)) * (cos(radians(azimuth_grid))) + (sin(radians(lead_dip))) * (cos(radians(lead_azimuth_grid))))) * ratio_factor AS y,
        --z
        ((((lead(depth_m, 1) OVER w) - depth_m) / 2) * (cos(radians(dip)) + (cos(radians(lead_dip))))) * ratio_factor AS z
    FROM
        surv
WINDOW w AS (PARTITION BY hole_id ORDER BY depth_m)
),
--generates the xyz positions
final AS (
    SELECT
        r.hole_id,
        lead(r.depth_m, 1) OVER (PARTITION BY r.hole_id ORDER BY r.hole_id,
            r.depth_m) AS depth_m,
    c.x + sum(r.x) OVER w_sum AS x,
        c.y + sum(r.y) OVER w_sum AS y,
            c.z - sum(r.z) OVER w_sum AS z
            FROM
                results r,
                collar c
            WHERE
                r.hole_id = c.hole_id
WINDOW w_sum AS (PARTITION BY r.hole_id ORDER BY r.hole_id,
    r.depth_m)
UNION ALL
SELECT
    hole_id,
    0::real AS depth_m,
    x,
    y,
    z
FROM
    collar
),
--remove values where depth_m is null
surv_xyz AS (
    SELECT
        *
    FROM
        final
    WHERE
        depth_m IS NOT NULL
),
--generate COMPOUNDCURVEZM geometry from points with ST_ForceCurve etc.
final_geom AS (
    SELECT
        trace.hole_id,
        public.ST_Transform (public.ST_SetSRID (public.ST_ForceCurve (public.ST_MakeLine (public.ST_MakePoint (x, y, z, depth_m))), srid), 4326) AS tmp_geom
FROM (
    SELECT
        hole_id,
        s.depth_m,
        s.x,
        s.y,
        s.z,
        srid
    FROM
        surv_xyz s
        JOIN collar USING (hole_id)
    ORDER BY
        hole_id, depth_m) trace
GROUP BY
    hole_id, srid)
--update the dh.collar table with geometry.
UPDATE
    dh.collar
SET
    geom_trace = tmp_geom
FROM
    final_geom
WHERE
    collar.hole_id = final_geom.hole_id
$function$
