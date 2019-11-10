SELECT 
  job_id, 
  AVG(salary) 
FROM 
  employees e, dept d 
WHERE 
  e.dept_id = d.dept_id 
  AND 1 = 1 
  AND e.salary BETWEEN (10000 + 1) AND 100000 * 10 
  AND e.bonus BETWEEN 100 + 2 AND (1000 * 15) 
GROUP BY 
  job_id 
HAVING 
  AVG(salary)< (
    SELECT 
      MAX(
        AVG(j.min_salary)
      ) 
    FROM 
      (
        select 
          * 
        from 
          jobs
      ) as j 
    WHERE 
      j.job_id IN (
        SELECT 
          jh.job_id 
        FROM 
          job_history jh FULL OUTER JOIN job_history_archive jha 
        WHERE jh.hist_id = jha.hist_id 
          AND jh.department_id BETWEEN 50 AND 100 
        ORDER BY 
          jh.job_id
      ) 
      AND j.job_id IN (
        SELECT 
          global_job_type 
        FROM 
          params
      ) 
    GROUP BY 
      j.job_id
  ) 
ORDER BY 
  d.dept_id 
LIMIT 
  10;

___________________________________________________________
SELECT 
  job_id, 
  AVG(salary) 
FROM 
  employees e, 
  (
    select 
      * 
    from 
      dept
  ) d 
WHERE 
  e.dept_id = d.dept_id 
  AND 1 = 1 
  AND e.salary BETWEEN (10000 + 1) AND 100000 * 10 
  AND e.bonus BETWEEN 100 + 2 AND (1000 * 15) 
GROUP BY 
  job_id 
HAVING 
  AVG(salary)< (
    SELECT 
      MAX(
        AVG(j.min_salary)
      ) 
    FROM 
      (
        select 
          * 
        from 
          jobs
      ) as j 
    WHERE 
      j.job_id IN (
        SELECT 
          jh.job_id 
        FROM 
          job_history jh, 
          (
            select 
              * 
            from 
              job_history_archive
          ) jha 
        WHERE jh.hist_id = jha.hist_id 
          AND jh.department_id BETWEEN 50 AND 100 
        ORDER BY 
          jh.job_id
      ) 
      AND j.job_id IN (
        SELECT 
          global_job_type 
        FROM 
          params
      ) 
    GROUP BY 
      j.job_id
  ) 
ORDER BY 
  d.dept_id 
LIMIT 
  10;

___________________________________________________________

SELECT 
  job_id, 
  AVG(salary) 
FROM 
  employees e, 
  (
    select 
      * 
    from 
      dept
  ) d 
WHERE 
  e.dept_id = d.dept_id 
  AND 1 = 1 
  AND e.salary BETWEEN (10000 + 1) 
  AND 100000 * 10 
  AND e.bonus BETWEEN 100 + 2 
  AND (1000 * 15) 
GROUP BY 
  job_id 
HAVING 
  AVG(salary)< (
    SELECT 
      MAX(
        AVG(j.min_salary)
      ) 
    FROM 
      (
        select 
          * 
        from 
          jobs
      ) as j 
    WHERE 
      j.job_id IN (
        SELECT 
          jh.job_id 
        FROM 
          job_history jh, 
          (
            select 
              * 
            from 
              job_history_archive
          ) jha 
        WHERE 
          jh.hist_id = jha.hist_id 
          AND jh.department_id BETWEEN 50 
          AND 100 
        ORDER BY 
          jh.job_id
      ) 
      AND j.job_id IN (
        SELECT 
          global_job_type 
        FROM 
          params
      ) 
    GROUP BY 
      j.job_id
  ) 
ORDER BY 
  d.dept_id 
LIMIT 
  10;

___________________________________________________________

select 
       nvl(a, b) 
from    				
  tab1 t1 
where 
  t1.id in (
    select 
      t2.id 
    from 
      tab2 t2 
    where 
      t2.id in (
        select 
          t3.id 
        from 
          tab3 t3 
        where 
          t3.id in (
            select 
              t4.id 
            from 
              tab4 t4 
            where 
              t4.name = 'foo' and (1=1)))) and exists (
    select 
      '1' 
    from 
      tab5 t5 
    where 
      t1.a = t5.b
  );
  
___________________________________________________________  

select 
  * 
from 
  (
    SELECT 
      v.name, 
      c.name, 
      p.lastname 
    FROM 
      vehicle v 
      INNER JOIN color c ON v.color_id = c.id 
      INNER JOIN person p ON v.person_id = p.id
  ) abc 
ORDER BY 
  name 
LIMIT 
  10;


___________________________________________________________
