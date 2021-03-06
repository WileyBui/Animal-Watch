def getActivityFeed(cur):
    cur.execute("""
        SELECT * FROM (
            SELECT
                Animals.id,
                Animals.species,
                Animals.imageURL,
                array_to_string(array_agg(distinct "tag"),'; ') AS tag,
                array_to_string(array_agg(distinct "tag_bootstrap_color"),'; ') AS tag_bootstrap_color
            FROM Animals, HasTag, Tags
            WHERE
                Animals.id = HasTag.animal_id
                AND HasTag.tag_id = Tags.id
            GROUP BY
                Animals.id,
                Animals.species,
                Animals.imageURL
        ) A
        ORDER BY A.id DESC;
    """)
    return cur
    
def getSharedContentsByAnimalId(cur, animal_id):
    # shared contents
    cur.execute("""
        SELECT
            Animals.species,
            array_to_string(array_agg(distinct "tag"),'; ') AS tag,
            array_to_string(array_agg(distinct "tag_bootstrap_color"),'; ') AS tag_bootstrap_color,
            Animals.imageURL
        FROM Animals, HasTag, Tags
        WHERE
            Animals.id = %s
            AND Animals.id = HasTag.animal_id
            AND HasTag.tag_id = Tags.id
        GROUP BY
            Animals.species,
            Animals.imageURL;
    """, [animal_id])
    return [record for record in cur]
        
def getAllPostsByAnimalId(cur, animal_id):
    # post contents
    cur.execute("""
        SELECT
            Users.users_name,
            Posts.post_text,
            Posts.imageURL,
            Posts.post_time,
            Posts.latitude,
            Posts.longitude,
            Users.profile_picture
        FROM Posts, Animals, Users
        WHERE
            Animals.id = %s
            AND Animals.id = Posts.animal_id
            AND Posts.users_id = Users.id;
    """, [animal_id])
    
    postList = [record for record in cur]
    
    # No posts created if nothing's returned; otherwise, gets the first index's contents
    postList = (["", "No post made...", None, None] if (len(postList) == 0) else postList)
    
    return postList

def getAllCommentsByAnimalId(cur, animal_id):
    # post contents
    cur.execute("""
        SELECT
            Users.users_name,
            Comments.comm_text,
            Comments.comm_time,
            Users.profile_picture,
            Comments.id,  --This is needed for edit/reply/report/delete
            Comments.users_id,   --This is needed for edit/report/delete
            Users.id    --This is needed for edit/report/delete
        FROM Animals, Comments, Users
        WHERE
            Animals.id = %s
            AND Animals.id = Comments.animal_id
            AND Comments.users_id = Users.id
        ORDER BY Comments.comm_time ASC;
    """, [animal_id])
    
    commentList = [record for record in cur]
    
    # No comments created if nothing's returned; otherwise, gets the first index's contents
    commentList = (["", "No comments made...", None, None] if (len(commentList) == 0) else commentList)
    
    return commentList