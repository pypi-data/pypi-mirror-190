from volworld_common.api.CA import CA
from volsite_postgres_common.db.BFn import BFn
from volsite_postgres_common.fn.function import AJsonPlPgSqlFunction, Arg


class FnHttpStatusError(AJsonPlPgSqlFunction):

    def name(self) -> str:
        return CFn.http_status_error

    '''
    [CA.HttpStatus]: SMALLINT
    [CA.Error]: JSONB
    '''
    def body(self) -> str:
        return (
            f" {Arg.result} := {BFn.jsonb_build_object}("
            f"    '{CA.HttpStatus}', ({Arg.input}->>'{CA.HttpStatus}')::SMALLINT, "
            f"    '{CA.Error}', ({Arg.input}->>'{CA.Error}')::JSONB"  
            f"  )"
        )