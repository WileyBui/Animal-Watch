def getActivityFeed(cur):
    cur.execute("""
        SELECT * FROM (
            SELECT
                Animals.id,
                Animals.species,
                Animals.image_id,
                array_to_string(array_agg(distinct "tag"),'; ') AS tag,
                array_to_string(array_agg(distinct "tag_bootstrap_color"),'; ') AS tag_bootstrap_color
            FROM Animals, HasTag, Tags
            WHERE
                Animals.id = HasTag.animal_id
                AND HasTag.tag_id = Tags.id
            GROUP BY
                Animals.id,
                Animals.species,
				Animals.image_id
        ) A
        ORDER BY A.ID DESC;
    """)
    return cur
    
def getSharedContentsByAnimalId(cur, animal_id):
    # shared contents
    cur.execute("""
        SELECT
            Animals.species,
            array_to_string(array_agg(distinct "tag"),'; ') AS tag,
            array_to_string(array_agg(distinct "tag_bootstrap_color"),'; ') AS tag_bootstrap_color,
            Animals.image_id,
			Animals.endangerment_level,
			Animals.animal_range,
			Animals.animal_description
        FROM Animals, HasTag, Tags
        WHERE
            Animals.id = %s
            AND Animals.id = HasTag.animal_id
            AND HasTag.tag_id = Tags.id
        GROUP BY
            Animals.species,
            Animals.image_id,
			Animals.endangerment_level,
			Animals.animal_range,
			Animals.animal_description;
    """, [animal_id])
    return [record for record in cur]
        
def getAllPostsByAnimalId(cur, animal_id):
    # post contents
    cur.execute("""
        SELECT
            Users.users_name,
            Posts.post_text,
            Posts.image_id,
            Posts.post_time,
            Posts.latitude,
            Posts.longitude,
            Users.profile_picture,
            Posts.id,
            Posts.users_id,
            Users.id
        FROM Posts, Animals, Users
        WHERE
            Animals.id = %s
            AND Animals.id = Posts.animal_id
            AND Posts.users_id = Users.id;
    """, [animal_id])
    
    postList = [record for record in cur]
    
    # No posts created if nothing's returned; otherwise, gets the first index's contents
    #postList = (["", "No post made...", None, None] if (len(postList) == 0) else postList)
    
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
    #commentList = (["", "No comments made...", None, None] if (len(commentList) == 0) else commentList)
    
    return commentList

def addTags(cur, animal_id, tagList):
    for tag in tagList:
        cur.execute("SELECT * FROM Tags WHERE Tags.tag = %s;", (tag,))
        tagExists = cur.fetchone()
        if tagExists:
            tag_id = tagExists[0]
        else:
            cur.execute("insert into Tags (tag, tag_bootstrap_color) values (%s, %s) RETURNING id;", (tag, 1))
            tag_id = cur.fetchone()[0]
        cur.execute("insert into HasTag (animal_id, tag_id) values (%s, %s);", (animal_id, tag_id))