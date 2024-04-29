--liquibase formatted sql

--changeset resume:1 rollbackSplitStatements:false
CREATE TABLE IF NOT EXISTS "person" (
    "id" BIGINT NOT NULL DEFAULT '0' PRIMARY KEY,
    "firstName" VARCHAR(255) NOT NULL DEFAULT '',
    "lastName" VARCHAR(255) NOT NULL DEFAULT '',
    "email" VARCHAR(255) NOT NULL DEFAULT '',
    "link1" VARCHAR(255) NOT NULL DEFAULT '',
    "link2" VARCHAR(255) NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_firstName ON "person" ("firstName");
CREATE INDEX IF NOT EXISTS idx_lastName ON "person" ("lastName");
-- rollback drop table "person";

--changeset resume:2 rollbackSplitStatements:false
CREATE TYPE "locationType" AS ENUM ('On-site', 'Remote');
CREATE TYPE "experience" AS ENUM ('Job','Co-op','Volunteer');
CREATE TABLE IF NOT EXISTS "position" (
    "id" BIGINT NOT NULL DEFAULT '0' PRIMARY KEY,
    "person_id" BIGINT NOT NULL DEFAULT '0',
    "company" VARCHAR(255) NOT NULL DEFAULT '',
    "startDate" TIMESTAMP NOT NULL DEFAULT '1970-01-01 00:00:00',
    "endDate" TIMESTAMP NULL DEFAULT NULL,
    "location" VARCHAR(255) NOT NULL DEFAULT '', 
    "locationType" "locationType" DEFAULT 'On-site',
    "experience" experience DEFAULT 'Job',
    "accomplishments" VARCHAR(255) ARRAY,
    "skillIds" BIGINT[]
);
CREATE INDEX IF NOT EXISTS idx_person_id ON "position" ("person_id");
CREATE INDEX IF NOT EXISTS idx_experience ON "position" ("experience");
CREATE INDEX IF NOT EXISTS idx_skillIds ON "position" USING GIN("skillIds");
-- rollback drop table "position";
-- rollback drop type "locationType";
-- rollback drop type "experience";

--changeset resume:3 rollbackSplitStatements:false
CREATE TYPE "skillType" AS ENUM ('hard','soft');
CREATE TABLE IF NOT EXISTS "skill" (
    "id" BIGINT NOT NULL DEFAULT '0' PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL DEFAULT '',
    "skillType" "skillType" DEFAULT 'hard'
);
CREATE INDEX IF NOT EXISTS idx_skillType ON "skill" ("skillType");
-- rollback drop table "skill";
-- rollback drop type "skillType";

--changeset resume:4 rollbackSplitStatements:false
CREATE TYPE "toolType" AS ENUM ('Software','Framework','Language');
CREATE TABLE IF NOT EXISTS "tool" (
    "id" BIGINT NOT NULL DEFAULT '0' PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL DEFAULT '',
    "toolType" "toolType" DEFAULT 'Software'
);
CREATE INDEX IF NOT EXISTS idx_toolType ON "tool" ("toolType");
-- rollback drop table "tool";
-- rollback drop type "toolType";

--changeset resume:5 rollbackSplitStatements:false
CREATE TYPE "educationType" AS ENUM ('BSc','BA','MSc','PhD');
CREATE TABLE IF NOT EXISTS "education" (
    "id" BIGINT NOT NULL DEFAULT '0' PRIMARY KEY,
    "person_id" BIGINT NOT NULL DEFAULT '0',
    "institution" VARCHAR(255) NOT NULL DEFAULT '',
    "degreeName" VARCHAR(255) NOT NULL DEFAULT '',
    "educationType" "educationType" DEFAULT 'BSc',
    "startDate" TIMESTAMP NOT NULL DEFAULT '1970-01-01 00:00:00',
    "endDate" TIMESTAMP NOT NULL DEFAULT '1970-01-01 00:00:00'
);
CREATE INDEX IF NOT EXISTS idx_person_id ON "education" ("person_id");
-- rollback drop table "education";
-- rollback drop type "educationType";
